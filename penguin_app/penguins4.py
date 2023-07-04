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

penguins_df = pd.read_csv('penguins.csv')
penguins_df = penguins_df[penguins_df['вид'] == selected_species]

fig, ax = plt.subplots()
ax = sns.scatterplot(x=penguins_df[selected_x_var],
                     y=penguins_df[selected_y_var])
plt.xlabel(selected_x_var)
plt.ylabel(selected_y_var)
plt.title("Диаграмма рассеяния для пингвинов вида {}".format(
    selected_species))
st.pyplot(fig)