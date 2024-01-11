import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Деревья Сан-Франциско')
st.write('Это приложение анализирует деревья в Сан-Франциско '
         'на основе набора данных, любезно предоставленного '
         'Департаментом общественных работ в Сан-Франциско')
st.subheader('График Plotly')
trees_df = pd.read_csv('trees.csv')

fig = px.histogram(trees_df['dbh'])
st.plotly_chart(fig)