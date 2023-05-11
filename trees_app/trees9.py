import streamlit as st
import pandas as pd
import altair as alt

st.title('Деревья Сан-Франциско')
st.write('Это приложение анализирует деревья в Сан-Франциско '
         'на основе набора данных, любезно предоставленного '
         'Департаментом общественных работ в Сан-Франциско')
trees_df = pd.read_csv('trees.csv')

fig = alt.Chart(trees_df).mark_bar().encode(
    x='caretaker', y='count(*):Q')
st.altair_chart(fig)