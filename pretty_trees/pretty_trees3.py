import streamlit as st
import pandas as pd

st.title('Деревья Сан-Франциско')
st.write('Это приложение анализирует деревья в Сан-Франциско '
         'на основе набора данных, любезно предоставленного '
         'Департаментом общественных работ в Сан-Франциско')
trees_df = pd.read_csv('trees.csv')

first_width = st.number_input('Ширина первой колонки', 
                              min_value=1, value=1)
second_width = st.number_input('Ширина второй колонки', 
                               min_value=1, value=1)
third_width = st.number_input('Ширина третьей колонки', 
                              min_value=1, value=1)

col1, col2, col3 = st.columns(
    (first_width, second_width, third_width))

with col1:
    st.write('Первая колонка')
    
with col2:
    st.write('Вторая колонка')

with col3:
    st.write('Третья колонка')