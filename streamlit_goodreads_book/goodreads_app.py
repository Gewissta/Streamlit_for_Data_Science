import streamlit as st
import pandas as pd

st.title("Анализируем ваши читательские привычки на Goodreads")
st.subheader("Веб-приложение [Тайлер Ричардс](http://www.tylerjrichards.com)")

"""
Привет! Добро пожаловать в приложение Tyler для анализа Goodreads. 
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
    
st.write(books_df.head())