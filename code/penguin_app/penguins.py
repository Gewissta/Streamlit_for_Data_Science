import streamlit as st
import pandas as pd

st.title("Пингвины Палмера")

# импортируем наши данные
penguins_df = pd.read_csv('penguins.csv')

# печатаем первые 5 наблюдений
st.write(penguins_df.head())