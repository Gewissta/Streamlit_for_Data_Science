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