import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_lottie import st_lottie
import requests

st.set_page_config(layout="wide")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

file_url = "https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json"
lottie_book = load_lottieurl(file_url)
st_lottie(lottie_book, speed=1, height=200, key="initial")

st.title("Анализируем ваши читательские привычки на Goodreads")
st.subheader("Веб-приложение [Тайлер Ричардс](http://www.tylerjrichards.com)")

"""
Привет! Добро пожаловать в приложение Тайлера для анализа Goodreads. 
Это приложение анализирует (и никогда не сохраняет!) книги, прочитанные 
вами с помощью популярного сервиса Goodreads, выводит распределение по 
"возрасту" и объему прочитанных вами книг. 
Попробуйте, загрузив свои данные ниже!
"""

goodreads_file = st.file_uploader(
    "Пожалуйста, импортируйте ваши данные Goodreads")
if goodreads_file is None:
    books_df = pd.read_csv("goodreads_history.csv")
    st.write("Анализируем историю Тайлера на Goodreads")
else:
    books_df = pd.read_csv(goodreads_file)
    st.write("Анализируем вашу историю на Goodreads")
    
# год прочтения книги
books_df["Год прочтения"] = pd.to_datetime(
    books_df["Дата начала чтения"]).dt.year
books_per_year = books_df.groupby(
    "Год прочтения")["Id книги"].count().reset_index()
books_per_year.columns = ["Год прочтения книги", "Количество"]
fig_year_finished = px.bar(
    books_per_year, 
    x="Год прочтения книги", 
    y="Количество", 
    title="Количество книг, прочитанных за год"
)

# разность дат
books_df['количество дней до завершения'] = (
    pd.to_datetime(books_df['Дата начала чтения']) - 
    pd.to_datetime(books_df['Дата добавления'])
).dt.days

# отфильтровываем данные
books_finished_filtered = books_df[
    (books_df['Эксклюзивная полка'] == 'read') & 
    (books_df['количество дней до завершения'] >= 0)
]
fig_days_finished = px.histogram(
    books_finished_filtered,
    x='количество дней до завершения', 
    title='Время между датой добавления и датой завершения',
    labels={'количество дней до завершения':'дни'})

# количество страниц
fig_num_pages = px.histogram(books_df, x='Количество страниц',
                             title='Гистограмма объема книги')

# год публикации
books_publication_year = books_df.groupby(
    'Год первоначальной публикации')['Id книги'].count().reset_index()
books_publication_year.columns = ['Год публикации', 'Count']

fig_year_published = px.bar(books_publication_year, x='Год публикации', 
                            y='Count', title='Гистограмма "возраста" книги')
fig_year_published.update_xaxes(range=[1850, 2021])

# рейтинг
books_rated = books_df[books_df['Мой рейтинг'] != 0]
fig_my_rating = px.histogram(
    books_rated, 
    x='Мой рейтинг', 
    title='Мой рейтинг')

fig_avg_rating = px.histogram(
    books_rated, 
    x='Средний рейтинг',
    title='Усредненный рейтинг пользователей Goodreads')

fig_avg_rating = px.histogram(
    books_rated, 
    x='Средний рейтинг', 
    title='Усредненный рейтинг пользователей Goodreads')

avg_difference = np.round(
    np.mean(books_rated['Мой рейтинг'] - books_rated['Средний рейтинг']), 2)

if avg_difference >= 0:
    sign = 'выше'
else:
    sign = 'ниже'
    
if goodreads_file is None:
    st.subheader("Результаты анализа Тайлера:")
else:
    st.subheader("Результаты вашего анализа:")
books_finished = books_df[books_df['Эксклюзивная полка'] == "read"]
u_books = len(books_finished['Id книги'].unique())
u_authors = len(books_finished['Автор'].unique())
mode_author = books_finished['Автор'].mode()[0]
st.write(
    f"Похоже, вы прочитали {u_books} книг, "
    f"общее количество уникальных авторов: {u_authors}. "
    f"Ваш самый читаемый автор – {mode_author}!"
)
st.write(
    "Результаты вашего приложения можно найти ниже. Мы проанализировали все: " 
    "от распределения объема ваших книг до того, как вы оцениваете книги. "
    "Посмотрите, все графики интерактивны!"
)

row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)
row3_col1, row3_col2 = st.columns(2)

with row1_col1:
    mode_year_finished = int(books_df['Год прочтения'].mode()[0])
    st.plotly_chart(fig_year_finished)
    st.write(f"Вы закончили чтение большинства книг в {mode_year_finished}. "
             f"Прекрасная работа!")

with row1_col2:
    st.plotly_chart(fig_days_finished)
    mean_days_to_finish = int(books_finished_filtered[
        'количество дней до завершения'].mean())
    st.write(
        f"Между добавлением книги в Goodreads и завершением ее прочтения "
        f"у вас проходит в среднем {mean_days_to_finish} дней. Это не "
        f"идеальная метрика, поскольку вы уже, возможно, положили "
        f"эту книгу в список книг, которые нужно прочитать!"
    )
with row2_col1:
    st.plotly_chart(fig_num_pages)
    avg_pages = int(books_df['Количество страниц'].mean())
    st.write(
        f"Объем прочитанных вами книг в среднем составляет "
        f"{avg_pages} страниц. Посмотрите распределение выше!"
    )
with row2_col2:
    st.plotly_chart(fig_year_published)
    st.write(
        "Эта диаграмма увеличена в масштабе для периода с 1850 по 2021 годы, " 
        "но она является интерактивной, поэтому попробуйте "
        "увеличить/уменьшить масштаб для интересных вам периодов!"
    )
with row3_col1:
    st.plotly_chart(fig_my_rating)
    avg_my_rating = round(books_rated['Мой рейтинг'].mean(), 2)
    st.write(f"Вы ставите книгам в среднем {avg_my_rating} звезды на Goodreads.")
with row3_col2:
    st.plotly_chart(fig_avg_rating)
    st.write(
        f"Вы оцениваете книги {sign}, чем средний пользователь "
        f"Goodreads на {abs(avg_difference)}!"
    )