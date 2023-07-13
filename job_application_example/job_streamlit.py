import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import requests

password_attempt = st.text_input("Пожалуйста, введите пароль")
if password_attempt != "example_password":
    st.write("Некорректный пароль!")
    st.stop()

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_airplane = load_lottieurl(
    "https://assets4.lottiefiles.com/packages/lf20_jhu1lqdz.json"
)
st_lottie(lottie_airplane, speed=1, height=200, key="initial")

st.title("Трудоустройство в крупную авиакомпанию США")
st.write("выполнено Тайлером Ричардсом")
st.subheader("Задание 1: Расстояние до аэропорта")

"""
Задание 1. Учитывая предложенный набор данных об аэропортах и 
местоположениях (по широте и долготе), напишите функцию, 
которая принимает код аэропорта в качестве входных данных 
и возвращает аэропорты, перечисленные от ближайшего 
к самому дальнему от аэропорта, поданного на вход.

Для это нам нужно выполнить 4 шага:
1. Загрузить данные
2. Реализовать алгоритм вычисления расстояний
3. Применить формулу вычисления расстояний ко всем аэропортам, 
кроме аэропорта, поданного на вход
4. Вернуть список аэропортов, отсортированных 
по возрастанию расстояния
"""

airport_distance_df = pd.read_csv("airport_location.csv")
st.write(airport_distance_df)

with st.echo():
    # загружаем необходимые данные
    airport_distance_df = pd.read_csv("airport_location.csv")

"""
Быстро погуглив, я обнаружил, что расстояние гаверсинусов является
хорошей аппроксимацией расстояния между двумя точками на сфере. 
По крайней мере, достаточно хорошей, чтобы получить расстояние между 
аэропортами! Расстояния по гаверсинусу могут отличаться до 0,5% 
от фактических, потому что Земля на самом деле не является сферой. 
Похоже, широта и долгота указаны в градусах, поэтому нужно найти 
способ учесть это. Формула гаверсинусов расстояния приведена ниже
с последующей реализацией на Python
"""
st.image("haversine.png")

with st.echo():
    from math import atan2, cos, radians, sin, sqrt

    def haversine_distance(long1, lat1, long2, lat2, degrees=False):
        # градусы и радианы
        if degrees == True:
            long1 = radians(long1)
            lat1 = radians(lat1)
            long2 = radians(long2)
            lat2 = radians(lat2)

        # реализуем формулу гаверсинусов
        a = (
            sin((lat2 - lat1) / 2) ** 2
            + cos(lat1) * cos(lat2) * sin((long2 - long1) / 2) ** 2
        )
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = 6371 * c  # радиус Земли в км
        return distance

# пишем функцию вычисления расстояний
# по формуле гаверсинусов
from math import atan2, cos, radians, sin, sqrt

def haversine_distance(long1, lat1,
                       long2, lat2,
                       degrees=False):
    # градусы и радианы
    if degrees == True:
        long1 = radians(long1)
        lat1 = radians(lat1)
        long2 = radians(long2)
        lat2 = radians(lat2)

    # реализуем формулу гаверсинусов
    a = (
        sin((lat2 - lat1) / 2) ** 2
        + cos(lat1) * cos(lat2) * sin((long2 - long1) / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # радиус Земли в км
    return distance

"""
Теперь нам нужно проверить нашу функцию! 
Расстояние между точками по умолчанию составляет
18998 километров, но не стесняйтесь задать
свои точки.
"""
long1 = st.number_input("Longitude 1", value=2.55)
long2 = st.number_input("Longitude 2", value=172.00)
lat1 = st.number_input("Latitude 1", value=49.01)
lat2 = st.number_input("Latitude 2", value=-43.48)

test_distance = haversine_distance(
    long1=long1, long2=long2, lat1=lat1, lat2=lat2, degrees=True
)
st.write("Ваше расстояние составляет: {} км".format(int(test_distance)))

"""
У нас реализована функция вычисления расстояний по формуле гаверсинусов, 
а также мы доказали себе, что она работает достаточно хорошо.
Наш следующий шаг — применить ее в нашей функции!
"""

with st.echo():
    def get_distance_list(airport_dataframe, airport_code):
        # создаем копию нашего фрейма данных 
        # для использования нашей функцией
        df = airport_dataframe.copy()
        # отбираем строку с введенным кодом аэропорта
        row = df[df.loc[:, "Airport Code"] == airport_code]
        # берем соответствующую широту и долготу
        lat = row["Lat"] 
        long = row["Long"]
        # отфильтровываем наш аэропорт
        df = df[df["Airport Code"] != airport_code]
        # вычисляем расстояния
        df["Distance"] = df.apply(
            lambda x: haversine_distance(
                lat1=lat, long1=long, lat2=x.Lat, long2=x.Long, degrees=True
            ),
            axis=1,
        )
        df_to_return = df.sort_values(
            by="Distance").reset_index()['Airport Code']
        # возращаем коды аэропортов по мере увеличения 
        # расстояния от нашего аэропорта
        return df_to_return

def get_distance_list(airport_dataframe,
                      airport_code):
    df = airport_dataframe.copy()
    row = df[df.loc[:, "Airport Code"] == airport_code]
    lat = row["Lat"]
    long = row["Long"]
    df = df[df["Airport Code"] != airport_code]
    df["Distance"] = df.apply(
        lambda x: haversine_distance(
            lat1=lat, long1=long, lat2=x.Lat, long2=x.Long, degrees=True
        ),
        axis=1,
    )
    df_to_return = df.sort_values(
        by="Distance").reset_index()['Airport Code']
    return df_to_return

"""    
Чтобы воспользоваться вышеприведенной функцией, выберите аэропорт 
из аэропортов, представленных в датафрейме, и приложение вернет
список аэропортов, от ближайшего до самого удаленного.
"""

selected_airport = st.selectbox(
    "Код аэропорта", 
    airport_distance_df["Airport Code"]
)
distance_airports = get_distance_list(
    airport_dataframe=airport_distance_df, airport_code=selected_airport
)
st.write("Ваши ближайшие аэропорты {}".format(list(distance_airports)))

"""
Все, кажется, работает просто отлично! Есть несколько способов улучшить 
решение, если бы было больше времени.
1. Я бы вместо расстояния гаверсинусов реализовал 
[Формулу Винсенти](https://en.wikipedia.org/wiki/Vincenty%27s_formulae), 
которая намного точнее, но громоздка в реализации.
2. Я бы векторизовал эту функцию и сделал бы ее более эффективной в целом.
Поскольку этот набор данных состоит всего из 7 строк, то это не имеет 
особого значения. Однако если бы это была важная функция, запускаемая 
в production, нужно ее векторизовать для ускорения.
"""

st.subheader("Задание 2: Представление данных")

"""
Я бы начал с нескольких вещей. Во-первых, я должен определить, 
какой на самом деле была уникальная поездка. Для этого я бы
выполнил группировку по месту отправления, пункту назначения 
и дате отправления (что касается даты отправления, часто клиенты 
меняют дату отправления, поэтому мы группируем по дате плюс-минус
как минимум 1 буферный день, чтобы зафиксировать все корректные даты).
Кроме того, мы видим, что часто пользователи ведут поиск по городу в целом,
а затем сокращают его, задав определенный аэропорт. Поэтому мы также
рассмотрим группу отдельных запросов из городов и аэропортов в одном и том
же городе в качестве одного и того же поиска и проделаем то же самое 
для пункта назначения. Мы добавим эти важные столбцы в каждый уникальный поиск.
"""

example_df = pd.DataFrame(
    columns=[
        "userid",
        "number_of_queries",
        "round_trip",
        "distance",
        "number_unique_destinations",
        "number_unique_origins",
        "datetime_first_searched",
        "average_length_of_stay",
        "length_of_search",
    ]
)
example_row = {
    "userid": 98593,
    "number_of_queries": 5,
    "round_trip": 1,
    "distance": 893,
    "number_unique_destinations": 5,
    "number_unique_origins": 1,
    "datetime_first_searched": "2015-01-09",
    "average_length_of_stay": 5,
    "length_of_search": 4,
}
st.write(example_df.append(example_row, ignore_index=True))

"""
Для ответа на вторую часть вопроса мы должны взять евклидово расстояние
по двум нормированным векторам. Есть два надежных варианта для сравнения двух
строк, состоящих из числовых значений, - евклидово расстояние (которое 
представляет собой просто прямую линию между двумя точками) и манхэттенское 
расстояние (вспомните пройденное расстояние, если вам пришлось использовать 
городские кварталы, чтобы пересечь Манхэттен по диагонали). Поскольку у нас 
есть нормированные данные, а данные не являются высокоразмерными или 
разреженными, я для начала рекомендовал бы использовать евклидово расстояние. 
Это расстояние показало бы, насколько схожи были две поездки.
"""