import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

st.title("Пингвины Палмера")

st.markdown("Используем это приложение Streamlit, чтобы создать " 
            "диаграмму рассеяния для анализа пингвинов!")

penguin_file = st.file_uploader(
    "Загрузите ваш CSV-файл с данными о пингвинах")

@st.cache_data
def load_file(penguin_file):
    time.sleep(3)
    if penguin_file is not None:
        df = pd.read_csv(penguin_file)
    else:
        df = pd.read_csv('penguins.csv')
    return(df)

penguins_df = load_file(penguin_file)

selected_x_var = st.selectbox(
    "Какую переменную отложить по оси x?",
    ["длина_клюва_мм", "высота_клюва_мм", 
     "длина_ласт_мм", "масса_тела_г"])

selected_y_var = st.selectbox(
    "Какую переменную отложить по оси y?",
    ["длина_клюва_мм", "высота_клюва_мм", 
     "длина_ласт_мм", "масса_тела_г"])

selected_gender = st.selectbox(
    "Пол",
    ["все", "мужская особь", "женская особь"])

if selected_gender == 'мужская особь':
    penguins_df = penguins_df[penguins_df['пол'] == 'мужская особь']
elif selected_gender == 'женская особь':
    penguins_df = penguins_df[penguins_df['пол'] == 'женская особь']
else:
    pass

sns.set_style('darkgrid')

fig, ax = plt.subplots()
ax = sns.scatterplot(x=penguins_df[selected_x_var],
                     y=penguins_df[selected_y_var],
                     hue=penguins_df['вид'])

plt.xlabel(selected_x_var)
plt.ylabel(selected_y_var)
plt.title("Диаграмма рассеяния для набора Пингвины Палмера: {}".format(
    selected_gender))
st.pyplot(fig)