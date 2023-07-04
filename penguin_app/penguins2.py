import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Пингвины Палмера")

st.markdown("Используем это приложение Streamlit, чтобы создать " 
            "диаграмму рассеяния для анализа пингвинов!")

selected_species = st.selectbox(
    "Какой вид пингвинов хотите визуализировать?",
    ["Adelie", "Gentoo", "Chinstrap"])

selected_x_var = st.selectbox(
    "Какую переменную отложить по оси x?",
    ["длина_клюва_мм", "высота_клюва_мм", 
     "длина_ласт_мм", "масса_тела_г"])

selected_y_var = st.selectbox(
    "Какую переменную отложить по оси y?",
    ["длина_клюва_мм", "высота_клюва_мм", 
     "длина_ласт_мм", "масса_тела_г"])