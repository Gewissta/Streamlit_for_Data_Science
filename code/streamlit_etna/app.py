# импортируем необходимые библиотеки
import pandas as pd
import numpy as np
import streamlit as st
import optuna

# импортируем классы ETNA
from etna.datasets import TSDataset
from etna.models import (CatBoostPerSegmentModel, 
                         CatBoostMultiSegmentModel)
from etna.transforms import (
    LogTransform,
    TimeSeriesImputerTransform,
    LinearTrendTransform,
    ChangePointsTrendTransform,
    TheilSenTrendTransform,
    LagTransform,
    DateFlagsTransform,
    FourierTransform,
    SegmentEncoderTransform,
    MeanTransform
)
from etna.metrics import SMAPE
from etna.pipeline import Pipeline
from etna.analysis import (plot_forecast,
                           plot_backtest,
                           plot_periodogram,
                           plot_trend)
from etna.auto import Tune

# отключаем вывод ненужного предупреждения
st.set_option("deprecation.showPyplotGlobalUse", False)

# задаем название приложения
st.title("Прогнозирование временных рядов с помощью ETNA")

# задаем заголовок раздела
st.header("Исходные данные")

# задаем поясняющий текст
st.write(
    "Данные должны быть в расплавленном, длинном формате. "
    "Столбец с метками времени должен называться **timestamp**. "
    "Метки времени должны быть в формате yyyy-mm-dd. "
    "Столбец с сегментами должен называться **segment**. "
    "Столбец с зависимой переменной должен называться **target**.")

# поле загрузки данных
data_file = st.file_uploader("Загрузите ваш CSV-файл")

# загружаем данные или останавливаем приложение
if data_file is not None:   
    data_df = pd.read_csv(data_file)
else:
    st.stop()
    
# выводим первые 10 наблюдений
st.dataframe(data_df)

# переводим данные в формат ETNA
df = TSDataset.to_dataset(data_df)
ts = TSDataset(df, freq="D")

# задаем заголовок раздела
st.header("Разведочный анализ рядов")

# радиокнопка - визуализировать ряды или нет
series_visualize = st.radio(
    "Визуализировать ряды?",
    ("Нет", "Да"))

# если не нужно визуализировать, ничего не делаем,
# а если нужно, строим график
if series_visualize == "Нет":
    pass
else:
    st.pyplot(ts.plot())
    
# радиокнопка - построить периодограмму или нет
periodogram_visualize = st.radio(
    "Построить периодограмму?",
    ("Нет", "Да"))

# если не нужно строить, ничего не делаем,
# а если нужно, строим периодограмму
if periodogram_visualize == "Нет":
    pass
else:
    st.pyplot(plot_periodogram(
        ts=ts, period=365.24,
        xticks=[1, 2, 4, 6, 12, 26, 52])
             )

# радиокнопка - визуализировать тренд или нет
trend_visualize = st.radio(
    "Визуализировать тренд?",
    ("Нет", "Да"))

# если не нужно визуализировать, ничего не делаем,
# а если нужно, визуализируем тренд (линейный, 
# кусочно-линейный, линейный, полученный с
# помощью оценки Тейла-Сена)
if trend_visualize == "Нет":
    pass
else:
    st.pyplot(plot_trend(
        ts=ts,
        trend_transform=[
            LinearTrendTransform(in_column='target'),
            ChangePointsTrendTransform(in_column='target'),
            TheilSenTrendTransform(in_column='target')])
             )

# задаем заголовок раздела
st.header("Горизонт прогнозирования")

# ввод горизонта прогнозирования
HORIZON = st.number_input(
    "Задайте горизонт прогнозирования", 
    min_value=1, value=14)

# разбиваем исторический набор на обучающий и тестовый
train_ts, test_ts = ts.train_test_split(
    test_size=HORIZON)

# записываем обучающий набор в обычном формате pandas
train_ts_init = train_ts.to_pandas(flatten=True)

# взглянем временные рамки наборов
st.write(f"временные рамки обучающего набора: "
         f"{train_ts.index[0].strftime('%Y-%m-%d')} - "
         f"{train_ts.index[-1].strftime('%Y-%m-%d')}")
st.write(f"временные рамки тестового набора: "
         f"{test_ts.index[0].strftime('%Y-%m-%d')} - "
         f"{test_ts.index[-1].strftime('%Y-%m-%d')}")

# радиокнопка - используем набор экзогенных переменных 
# для обучающего набора или нет
train_exog_exist = st.radio(
    "Есть набор экзогенных переменных для обучающего набора?",
    ("Нет", "Да"))

# либо ничего не делаем, либо загружаем набор 
# экзогенных переменных для обучающего набора
if train_exog_exist == "Нет":
    pass
else:
    # задаем заголовок раздела
    st.header("Набор экзогенных переменных для обучающего набора")
    
    # задаем поясняющий текст
    st.write(
        "Данные должны быть в расплавленном, длинном формате. "
        "Столбец с метками времени должен называться **timestamp**. "
        "Метки времени должны быть в формате yyyy-mm-dd. "
        "Столбец с сегментами должен называться **segment**. "
        "Последняя дата набора - это последняя дата обучающего набора + "
        "H периодов, где H - горизонт прогнозирования. Предполагается, что "
        "значения всех переменных известны в будущем (циклические признаки "
        "времени, качественные характеристики товаров/магазинов и т.д.). "
        "Этот набор экзогенных переменных можно использовать для построения "
        "базовой модели на обучающем наборе и перекрестной проверки, "
        "запускаемой на обучающем наборе."
    )

    # поле загрузки данных
    train_exog_file = st.file_uploader(
        "Загрузите ваш CSV-файл с экзогенными "
        "переменными для обучающего набора"
    )
    
    # если набор экзогенных переменных не загружен, 
    # останавливаем приложение
    if train_exog_file is None:
        st.stop()
    # если набор экзогенных переменных загружен,
    # выполняем следующие действия
    else:
        # прочитываем в датафрейм
        train_exog = pd.read_csv(train_exog_file)
        
        # выводим первые 10 наблюдений
        st.dataframe(train_exog.head(10))
        
        train_ts = train_ts.to_pandas(flatten=True)
        
        # создаем объединенный набор
        train_ts = TSDataset(
            df=TSDataset.to_dataset(train_ts), 
            df_exog=TSDataset.to_dataset(train_exog),
            freq='D', known_future='all'
        )   

# задаем заголовок раздела
st.header("Преобразования зависимой переменной")

# задаем список классов, ответственных за преобразования
tf_classes_options = ["LogTransform", 
                      "TimeSeriesImputerTransform", 
                      "LinearTrendTransform"]

# создаем в боковой панели поле множественного выбора 
# классов, ответственных за преобразования, на выходе - 
# список выбранных классов, ответственных за преобразования
tf_classes_lst = st.sidebar.multiselect(
    "Список классов, создающих преобразования", tf_classes_options)

# пустой словарь для классов, ответственных за преобразования
tf_classes_dict = {}

# проверяем наличие соответствующего класса в списке выбранных
# классов, ответственных за преобразования, и обновляем словарь
if "LogTransform" in tf_classes_lst: 
    log = LogTransform(in_column="target")
    
    tf_classes_dict.update({"LogTransform": log})
    
if "TimeSeriesImputerTransform" in tf_classes_lst:
    
    imputer_title = (
        "<p style='font-family:Arial; color:Black; font-size: 18px;'" + 
        ">Выберите настройки для TimeSeriesImputerTransform</p>")
    st.markdown(imputer_title, unsafe_allow_html=True)
    
    # поле выбора - стратегия импутации пропусков
    strategy = st.selectbox(
    "Стратегия импутации пропусков",
    ["constant", "mean", "running_mean", 
     "seasonal", "forward_fill"])
    
    # два числовых ввода - ширина скользящего окна и сезонность
    window = st.number_input(
        "Введите ширину скользящего окна", min_value=-1)
    seasonality = st.number_input(
        "Введите длину сезонности", min_value=1)
       
    imputer = TimeSeriesImputerTransform(
        in_column="target", 
        strategy=strategy,
        window=window,
        seasonality=seasonality)
    
    tf_classes_dict.update({"TimeSeriesImputerTransform": imputer})
    
if "LinearTrendTransform" in tf_classes_lst: 
    detrend = LinearTrendTransform(in_column="target")
    
    tf_classes_dict.update({"LinearTrendTransform": detrend})

# формируем итоговый список значений из словаря, в который 
# положили выбранные классы, ответственные за преобразования
final_tf_classes_lst = list(tf_classes_dict.values())

# задаем заголовок раздела
st.header("Конструирование признаков")

# задаем список классов, ответственных за создание признаков
fe_classes_options = ["LagTransform", "MeanTransform", 
                      "DateFlagsTransform", "FourierTransform",
                      "SegmentEncoderTransform"]

# создаем в боковой панели поле множественного выбора классов, 
# ответственных за создание признаков, на выходе - список 
# выбранных классов, ответственных за создание признаков
fe_classes_lst = st.sidebar.multiselect(
    'Список классов, создающих признаки', fe_classes_options)

# пустой словарь для классов, ответственных за создание признаков
fe_classes_dict = {}

# проверяем наличие соответствующего класса в списке выбранных
# классов, ответственных за создание признаков, и обновляем словарь
if "LagTransform" in fe_classes_lst:   
    lags_title = (
        "<p style='font-family:Arial; color:Black; font-size: 18px;'" + 
        ">Выберите настройки для LagTransform</p>")
    st.markdown(lags_title, unsafe_allow_html=True)
    
    # три числовых ввода - нижняя граница порядка лага, 
    # верхняя граница лага, шаг прироста порядка лага
    lower_limit = st.number_input("Нижняя граница порядка лага", 
                                  min_value=HORIZON)
    increment = st.number_input("Шаг прироста порядка лага", 
                                min_value=1, value=int(np.sqrt(HORIZON)))   
    upper_limit = st.number_input("Верхняя граница порядка лага", 
                                  min_value=HORIZON + increment,
                                  value=2 * HORIZON)
    lags = LagTransform(in_column="target", 
                        lags=list(range(lower_limit, upper_limit, increment)), 
                        out_column="target_lag")
    
    fe_classes_dict.update({"LagTransform": lags})
    
if "MeanTransform" in fe_classes_lst:   
    means_title = (
        "<p style='font-family:Arial; color:Black; font-size: 18px;'" + 
        ">Выберите настройки для MeanTransform</p>")
    st.markdown(means_title, unsafe_allow_html=True)
    
    # поле числового ввода - количество скользящих окон
    means_number = st.number_input("Введите количество окон", min_value=1)
    # слайдер - настройка ширины конкретного скользящего окна 
    numbers = [st.slider(f"Введите ширину {i+1}-го окна", 
                         min_value=HORIZON, 
                         max_value=3 * HORIZON)
               for i in range(means_number)] 
    
    for number in numbers:
        fe_classes_dict.update({f"MeanTransform{number}": MeanTransform(
            in_column="target",
            window=number, 
            out_column=f"target_mean{number}")})
        
if "FourierTransform" in fe_classes_lst:   
    fourier_title = (
        "<p style='font-family:Arial; color:Black; font-size: 18px;'" + 
        ">Выберите настройки для FourierTransform</p>")
    st.markdown(fourier_title, unsafe_allow_html=True)
    # два числовых ввода - период и порядок
    period = st.number_input("Период сезонности", min_value=0.0, 
                             value=365.25, max_value=365.25)
    order = st.number_input("Порядок компонент Фурье", min_value=1, 
                            value=3, max_value=30)
    fourier = FourierTransform(period=period, 
                               order=order, 
                               out_column="fourier")
    fe_classes_dict.update({"FourierTransform": fourier})

if "DateFlagsTransform" in fe_classes_lst:
    dateflags_title = (
        "<p style='font-family:Arial; color:Black; font-size: 18px;'" + 
        ">Выберите настройки для DateFlagsTransform</p>")
    st.markdown(dateflags_title, unsafe_allow_html=True)
    
    # флаги - календарные признаки
    day_number_in_week = st.checkbox(
        "Порядковый номер дня в неделе", 
        value=False)   
    day_number_in_month = st.checkbox(
        "Порядковый номер дня в месяце", 
        value=True)
    week_number_in_month = st.checkbox(
        "Порядковый номер недели в месяце", 
        value=False)  
    month_number_in_year = st.checkbox(
        "Порядковый номер месяца в году", 
        value=True)
    season_number = st.checkbox(
        "Порядковый номер сезона в году", 
        value=False)
    is_weekend = st.checkbox(
        "Индикатор выходного дня", 
        value=False)
    
    dateflags = DateFlagsTransform(
        day_number_in_week=day_number_in_week,
        day_number_in_month=day_number_in_month,
        week_number_in_month=week_number_in_month,
        month_number_in_year=month_number_in_year,
        season_number=season_number,
        is_weekend=is_weekend,
        out_column="date_flag")
    
    fe_classes_dict.update({"DateFlagsTransform": dateflags})

if "SegmentEncoderTransform" in fe_classes_lst:
    seg = SegmentEncoderTransform()   
    fe_classes_dict.update({"SegmentEncoderTransform": seg})

# формируем итоговый список значений из словаря, в который 
# положили выбранные классы, ответственные за создание признаков    
final_fe_classes_lst = list(fe_classes_dict.values())

# объединяем список классов, выполняющих преобразования, 
# и список классов, создающих признаки
final_classes_lst = final_tf_classes_lst + final_fe_classes_lst

# формируем список классов, создающих признаки по умолчанию,
# когда эти классы не заданы нами вручную
default_lags = LagTransform(
    in_column="target", 
    lags=list(range(HORIZON, 3 * HORIZON, HORIZON)), 
    out_column="target_lag")

default_dateflags = DateFlagsTransform(
    day_number_in_week=True,
    week_number_in_month=True, 
    month_number_in_year=True,
        out_column="date_flag")

default_classes_lst = [default_lags, default_dateflags]

# если классы, создающие признаки, не заданы вручную,
# формируем список классов по умолчанию, в противном
# случае используем объединенный список, созданный
# выше
if len(final_fe_classes_lst) == 0:
    transforms = default_classes_lst
else:
    transforms = final_classes_lst
    
# задаем заголовок раздела
st.header("Список экземпляров классов, выполняющих преобразования "
          "зависимой переменной и создающих признаки")

# список экземпляров классов
st.write(transforms)
    
# задаем заголовок раздела  
st.header("Итоговый набор")

# задаем поясняющий текст
st.write(
    "Лаги, скользящие статистики, члены ряда Фурье, календарные "
    "признаки создаются во время обучения."
)

# выводим итоговый набор
st.dataframe(train_ts)

# задаем заголовок раздела
st.header("Обучение базовой модели CatBoost")

# поля числового ввода - значения основных
# гиперпараметров модели CatBoost
iterations = st.number_input(
    "Введите количество деревьев",
    min_value=1, max_value=2000, value=200)
learning_rate = st.number_input(
    "Введите темп обучения", 
    min_value=0.001, max_value=1.0, value=0.03)
depth = st.number_input(
    "Введите максимальную глубину деревьев", 
    min_value=1, max_value=16, value=6)

# задаем выбор типа модели CatBoost с помощью поля
# одиночного выбора в боковой панели
catboost_model_type = st.sidebar.selectbox(
    "Какую модель CatBoost обучить?",
    ["PerSegment", "MultiSegment"])
  
if catboost_model_type == "PerSegment":
    # создаем модель CatBoostPerSegmentModel
    model = CatBoostPerSegmentModel(
        iterations=iterations,
        learning_rate=learning_rate,
        depth=depth)
else:
    # создаем модель CatBoostMultiSegmentModel
    model = CatBoostMultiSegmentModel(
        iterations=iterations,
        learning_rate=learning_rate,
        depth=depth)
    
# радиокнопка - строить базовую модель или нет
run_model = st.radio(
    "Обучить базовую модель?",
    ("Нет", "Да"))

# либо останавливаем приложение, либо строим модель
if run_model == "Нет":
    st.stop()
else:
    pass

# создаем конвейер
pipeline = Pipeline(model=model, 
                    transforms=transforms, 
                    horizon=HORIZON)
# обучаем конвейер
pipeline.fit(train_ts)
# получаем прогнозы
forecast_ts = pipeline.forecast()

# создаем экземпляр класса SMAPE
smape = SMAPE()
# вычисляем метрики по сегментам
smape_values = smape(y_true=test_ts, 
                     y_pred=forecast_ts)
# кладем метрики по сегментам в датафрейм 
# и даем имя столбцу с ними
smape_values = pd.DataFrame({"Прогнозы": smape_values})
# вычисляем среднее значение SMAPE
smape_mean = smape_values["Прогнозы"].mean()

# задаем заголовок раздела
st.header("Оценка качества прогнозов базовой модели - SMAPE")
# печатаем метрики по сегментам и среднее значение метрики
st.write(smape_values)
st.write("Среднее значение:", smape_mean)

# задаем заголовок раздела
st.header("Визуализация прогнозов базовой модели")

# слайдер - количество последних наблюдений в обучающей выборке
n_train_samples = st.slider(
    "N последних наблюдений в обучающей выборке", 
    min_value=3 * HORIZON)

# строим график прогнозов
st.pyplot(
    plot_forecast(
        forecast_ts=forecast_ts,
        test_ts=test_ts,
        train_ts=train_ts,
        n_train_samples=n_train_samples,
    )
)

# задаем заголовок раздела
st.header("Перекрестная проверка модели")

# поля одиночного выбора и числового ввода
# - настройки перекрестной проверки
mode = st.selectbox(
    "Стратегия перекрестной проверки",
    ["expand", "constant"])

n_folds = st.number_input(
    "Введите количество блоков перекрестной проверки", 
    min_value=1, max_value=24, value=3)

# радиокнопка - запускать перекрестную проверку или нет
run_cv = st.radio(
    "Запустить перекрестную проверку?",
    ("Нет", "Да"))

# либо останавливаем приложение, либо 
# запускаем перекрестную проверку
if run_cv == "Нет":
    st.stop()
else:
    pass

# радиокнопка - выбор способа запуска перекрестной проверки
run_cv_method = st.radio(
    "Как запустить перекрестную проверку?",
    ("На обучающем наборе", "На всем историческом наборе"))
    
if run_cv_method == "На обучающем наборе":
    # радиокнопка - используем набор экзогенных переменных 
    # для перекрестной проверки на обучающем наборе или нет
    tr_exg_exist = st.radio(
        "Есть набор экзогенных переменных для перекрестной "
        "проверки на обучающем наборе?",
        ("Нет", "Да"))

    # либо сразу запускаем перекрестную проверку для обучающем наборе, 
    # либо загружаем набор экзогенных переменных для перекрестной 
    # проверки на обучающем наборе
    if tr_exg_exist == "Нет":
        
        tr = TSDataset.to_dataset(train_ts_init)
        tr = TSDataset(tr, freq="D")
        st.header("Итоговый набор")
        st.dataframe(tr)
        
        # находим метрики и прогнозы моделей по сегментам по
        # итогам перекрестной проверки на обучающем наборе
        metrics_cv, forecast_cv, _ = pipeline.backtest(
            mode=mode, 
            n_folds=n_folds,
            ts=tr, 
            metrics=[smape], 
            aggregate_metrics=True)
        
    else:
        # задаем заголовок раздела
        st.header("Набор экзогенных переменных для перекрестной "
                  "проверки на обучающем наборе")
    
        # задаем поясняющий текст
        st.write(
            "Данные должны быть в расплавленном, длинном формате. "
            "Столбец с метками времени должен называться **timestamp**. "
            "Метки времени должны быть в формате yyyy-mm-dd. "
            "Столбец с сегментами должен называться **segment**. "
            "Последняя дата набора - это последняя дата обучающего набора + "
            "H периодов, где H - горизонт прогнозирования. Предполагается, что "
            "значения всех переменных известны в будущем (циклические признаки "
            "времени, качественные характеристики товаров/магазинов и т.д.). "
        )

        # поле загрузки данных
        tr_exg_file = st.file_uploader(
            "Загрузите ваш CSV-файл с экзогенными переменными для "
            "перекрестной проверки на обучающем наборе"
        )
    
        # если набор экзогенных переменных не загружен, 
        # останавливаем приложение
        if tr_exg_file is None:
            st.stop()
        # если набор экзогенных переменных загружен,
        # выполняем следующие действия
        else:
            # прочитываем в датафрейм
            tr_exg = pd.read_csv(tr_exg_file)
        
            # выводим первые 10 наблюдений
            st.dataframe(tr_exg.head(10))
        
            # создаем объединенный набор
            tr_exog = TSDataset(
                df=TSDataset.to_dataset(train_ts_init), 
                df_exog=TSDataset.to_dataset(tr_exg),
                freq='D', known_future='all'
            )   
            st.header("Итоговый набор")
            st.dataframe(tr_exog)
            
            # находим метрики и прогнозы моделей по сегментам 
            # по итогам перекрестной проверки на обучающем
            # наборе (с экзогенными переменными)
            metrics_cv, forecast_cv, _ = pipeline.backtest(
                mode=mode, 
                n_folds=n_folds,
                ts=tr_exog, 
                metrics=[smape], 
                aggregate_metrics=True)
    
else:    
    # радиокнопка - используем набор экзогенных переменных 
    # для перекрестной проверки на всем историческом 
    # наборе или нет
    ts_exg_exist = st.radio(
        "Есть набор экзогенных переменных для перекрестной "
        "проверки на всем историческом наборе?",
        ("Нет", "Да"))

    # либо ничего не делаем, либо загружаем набор экзогенных 
    # переменных для перекрестной проверки на всем
    # историческом наборе
    if ts_exg_exist == "Нет":
        
        st.header("Итоговый набор")
        st.dataframe(ts)
        
        # находим метрики и прогнозы моделей по сегментам по
        # итогам перекрестной проверки на всем историческом
        # наборе
        metrics_cv, forecast_cv, _ = pipeline.backtest(
            mode=mode, 
            n_folds=n_folds,
            ts=ts, 
            metrics=[smape], 
            aggregate_metrics=True) 
    else:
        # задаем заголовок раздела
        st.header("Набор экзогенных переменных для перекрестной "
                  "проверки на всем историческом наборе")
    
        # задаем поясняющий текст
        st.write(
            "Данные должны быть в расплавленном, длинном формате. "
            "Столбец с метками времени должен называться **timestamp**. "
            "Метки времени должны быть в формате yyyy-mm-dd. "
            "Столбец с сегментами должен называться **segment**. "
            "Последняя дата набора - это последняя дата исторического набора + "
            "H периодов, где H - горизонт прогнозирования. Предполагается, что "
            "значения всех переменных известны в будущем (циклические признаки "
            "времени, качественные характеристики товаров/магазинов и т.д.)."
        )

        # поле загрузки данных
        ts_exg_file = st.file_uploader(
            "Загрузите ваш CSV-файл с экзогенными переменными для "
            "перекрестной проверки на всем историческом наборе"
        )
    
        # если набор экзогенных переменных не загружен, 
        # останавливаем приложение
        if ts_exg_file is None:
            st.stop()
        # если набор экзогенных переменных загружен,
        # выполняем следующие действия
        else:
            # прочитываем в датафрейм
            ts_exg = pd.read_csv(ts_exg_file)
        
            # выводим первые 10 наблюдений
            st.dataframe(ts_exg.head(10))
        
            ts_init = ts.to_pandas(flatten=True)
        
            # создаем объединенный набор
            ts_exog = TSDataset(
                df=TSDataset.to_dataset(ts_init), 
                df_exog=TSDataset.to_dataset(ts_exg),
                freq='D', known_future='all'
            )   
            st.header("Итоговый набор")
            st.dataframe(ts_exog)
            
            # находим метрики и прогнозы моделей по сегментам по
            # итогам перекрестной проверки на всем историческом
            # наборе (c экзогенными переменными)
            metrics_cv, forecast_cv, _ = pipeline.backtest(
                mode=mode, 
                n_folds=n_folds,
                ts=ts_exog, 
                metrics=[smape], 
                aggregate_metrics=True)
    
# вычисляем среднее значение метрики по сегментам
cv_mean_smape = metrics_cv['SMAPE'].mean()

# задаем заголовок раздела
st.header("Оценка качества прогнозов по итогам " 
          "перекрестной проверки - SMAPE")

# печатаем метрики по сегментам и среднее значение метрики
st.write(metrics_cv)
st.write("Среднее значение:", cv_mean_smape)

# задаем заголовок раздела
st.header("Визуализация прогнозов по итогам перекрестной проверки")

if run_cv_method == "На обучающем наборе":
    # визуализируем результаты перекрестной проверки
    st.pyplot(
        plot_backtest(forecast_cv, train_ts, history_len=0)
    )
else:
    # визуализируем результаты перекрестной проверки
    st.pyplot(
        plot_backtest(forecast_cv, ts, history_len=0)
    )

# задаем заголовок раздела
st.header("Оптимизация гиперпараметров")

# радиокнопка - настроить оптимизацию гиперпараметров или нет
hyperparams_tune = st.radio(
    "Настроить оптимизацию гиперпараметров?",
    ("Нет", "Да"))

# либо останавливаем приложение, либо 
# запускаем настройку гиперпараметров
if hyperparams_tune == "Нет":
    st.stop()
else:
    pass

# радиокнопка - вывести структуру конвейера или нет
pipeline_output = st.radio(
    "Вывести структуру конвейера?",
    ("Нет", "Да"))

# не печатаем или печатаем структуру конвейера
if pipeline_output == "Нет":
    pass
else:
    # печатаем структуру конвейера
    st.write("Структура конвейера:", pipeline.to_dict())

# радиокнопка - вывести сетку гиперпараметров или нет
hyperparams_grid_output = st.radio(
    "Вывести сетку гиперпараметров?",
    ("Нет", "Да"))

# не печатаем или печатаем сетку гиперпараметров
if hyperparams_grid_output == "Нет":
    pass
else:
    # печатаем сетку гиперпараметров
    st.write("Сетка гиперпараметров:", pipeline.params_to_tune())

optim_cv_settings_title = (
    "<p style='font-family:Arial; color:Black; font-size: 18px;'" + 
    ">Настройки перекрестной проверки для оптимизации</p>")
st.markdown(optim_cv_settings_title, unsafe_allow_html=True)    
    
# поле одиночного выбора и поле числового ввода
# - настройки перекрестной проверки
# для оптимизации
optim_cv_mode = st.selectbox(
    "Стратегия перекрестной проверки для оптимизации",
    ["expand", "constant"])

optim_cv_n_folds = st.number_input(
    "Введите количество блоков перекрестной проверки для оптимизации", 
    min_value=1, max_value=20, value=5)

# создаем оптимизатор - экземпляр класса Tune,
# используя сетку гиперпараметров по умолчанию
tune = Tune(pipeline=pipeline, 
            target_metric=SMAPE(),
            storage='sqlite:///Tune_results.db',
            horizon=HORIZON, 
            backtest_params=dict(mode=optim_cv_mode,
                                 n_folds=optim_cv_n_folds))

optim_settings_title = (
    "<p style='font-family:Arial; color:Black; font-size: 18px;'" + 
    ">Настройки процесса оптимизации и вывода результатов</p>")
st.markdown(optim_settings_title, unsafe_allow_html=True)  

# ввод количества итераций оптимизации
n_trials = st.number_input(
    "Введите количество итераций оптимизации", 
    min_value=1, value=10, max_value=1000)

# количество наилучших конвейеров, выводимых
# по итогам оптимизации
top_k = st.number_input(
    "Введите количество наилучших конвейеров для вывода", 
    min_value=1, max_value=20, value=3)

# радиокнопка - запустить оптимизацию гиперпараметров или нет
hyperparams_optim_run = st.radio(
    "Запустить оптимизацию гиперпараметров? "
    "(Запускается на всем историческом наборе)", 
    ("Нет", "Да")
)

# либо останавливаем приложение, либо 
# запускаем оптимизацию гиперпараметров
if hyperparams_optim_run == "Нет":
    st.stop()
else:
    # радиокнопка - есть экзогенные переменные или нет
    exogenous_exist = st.radio(
        "Исторический набор содержит экзогенные переменные?",
        ("Нет", "Да")
    )
    
    if exogenous_exist == "Нет":
        # запускаем сессию оптимизации Optuna
        # на историческом наборе
        tune.fit(ts=ts, n_trials=n_trials)
    else:
        # запускаем сессию оптимизации Optuna
        # на историческом наборе
        # c экзоненными переменными
        tune.fit(ts=ts_exog, n_trials=n_trials)
        
    # выводим сводку, убрав дубликаты
    tune_results_tbl = tune.summary()[
        ["hash", "pipeline", "SMAPE_mean", "state"]
    ].sort_values("SMAPE_mean").drop_duplicates(subset="hash")
    st.write("Результаты оптимизации:", tune_results_tbl)

    # выведем k лучших конвейеров
    top_k_pipelines = tune.top_k(k=top_k)
    st.write("Лучшие конвейеры:", top_k_pipelines)

    # задаем заголовок раздела
    st.header("Прогнозы для новых данных")

    # радиокнопка - вычислить прогнозы для новых данных или нет
    calc_forecasts = st.radio(
        "Вычислить прогнозы для новых данных?",
        ("Нет", "Да"))

    # либо останавливаем приложение, либо вычисляем прогнозы
    if calc_forecasts == "Нет":
        st.stop()
    else:
        # записываем наилучший конвейер
        best_pipeline = top_k_pipelines[0]
        # обучаем конвейер на всем наборе
        best_pipeline.fit(ts)
        # получаем прогнозы
        best_pipeline_forecast_ts = best_pipeline.forecast()
        # переводим в плоский формат и отбираем интересующие столбцы
        flatten_forecast_ts = best_pipeline_forecast_ts.to_pandas(flatten=True)
        forecasts = flatten_forecast_ts[["timestamp", "segment", "target"]] 
        # выводим прогнозы
        st.dataframe(forecasts)

    # радиокнопка - записать прогнозы в CSV-файл или нет
    csv_file = st.radio(
        "Записать прогнозы для новых данных в CSV-файл?",
        ("Нет", "Да"))

    # либо ничего не делаем, либо записываем 
    # прогнозы для новых данных в CSV-файл
    if csv_file == "Нет":
        st.stop()
    else:
        forecasts.to_csv("predictions.csv", index=False)  