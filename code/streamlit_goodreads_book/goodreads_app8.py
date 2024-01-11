import streamlit as st
import pandas as pd
import plotly.express as px

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
st.plotly_chart(fig_year_finished)

# разность дат
books_df["количество дней до завершения"] = (
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
st.plotly_chart(fig_days_finished)

fig_num_pages = px.histogram(books_df, x='Количество страниц',
                             title='Гистограмма объема книги')
st.plotly_chart(fig_num_pages)

books_publication_year = books_df.groupby(
    'Год первоначальной публикации')['Id книги'].count().reset_index()
books_publication_year.columns = ['Год публикации', 'Count']
st.write(books_df.sort_values(by='Год первоначальной публикации').head())
fig_year_published = px.bar(books_publication_year, x='Год публикации', 
                            y='Count', title='Гистограмма "возраста" книги')
fig_year_published.update_xaxes(range=[1850, 2021])
st.plotly_chart(fig_year_published)
st.write('Эта диаграмма увеличена в масштабе для периода с 1850 по 2021 годы, ' 
         'но она является интерактивной, поэтому попробуйте '
         'увеличить/уменьшить масштаб для интересных вам периодов!')

books_rated = books_df[books_df['Мой рейтинг'] != 0]
fig_my_rating = px.histogram(
    books_rated, 
    x='Мой рейтинг', 
    title='Мой рейтинг')
st.plotly_chart(fig_my_rating)
fig_avg_rating = px.histogram(
    books_rated, 
    x='Средний рейтинг',
    title='Усредненный рейтинг пользователей Goodreads')
st.plotly_chart(fig_avg_rating)

fig_avg_rating = px.histogram(
    books_rated, 
    x='Средний рейтинг', 
    title='Усредненный рейтинг пользователей Goodreads')
st.plotly_chart(fig_avg_rating)

import numpy as np

avg_difference = np.round(
    np.mean(books_rated['Мой рейтинг'] - books_rated['Средний рейтинг']), 2)

if avg_difference >= 0:
    sign = 'выше'
else:
    sign = 'ниже'
st.write(f"Вы оцениваете книги {sign}, чем средний пользователь " 
         f"Goodreads на {abs(avg_difference)}!")