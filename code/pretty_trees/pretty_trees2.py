import streamlit as st
import pandas as pd

st.title('Деревья Сан-Франциско')
st.write('Это приложение анализирует деревья в Сан-Франциско '
         'на основе набора данных, любезно предоставленного '
         'Департаментом общественных работ в Сан-Франциско')
trees_df = pd.read_csv('trees.csv')

col1, col2, col3 = st.columns((1,1,1))
col1.write('Первая колонка')
col2.write('Вторая колонка')
col3.write('Третья колонка')