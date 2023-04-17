import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Пингвины Палмера")

st.markdown("Используем это приложение Streamlit, чтобы создать " 
            "диаграмму рассеяния для анализа пингвинов!")

selected_x_var = st.selectbox(
    "Какую переменную отложить по оси x?",
    ["длина_клюва_мм", "высота_клюва_мм", 
     "длина_ласт_мм", "масса_тела_г"])

selected_y_var = st.selectbox(
    "Какую переменную отложить по оси y?",
    ["длина_клюва_мм", "высота_клюва_мм", 
     "длина_ласт_мм", "масса_тела_г"])

penguin_file = st.file_uploader(
    "Загрузите ваш CSV-файл с данными о пингвинах")

if penguin_file is not None:
    penguins_df = pd.read_csv(penguin_file)
else:
    st.stop()
    
sns.set_style('darkgrid')

markers = {"Adelie": "X", "Gentoo": "s", "Chinstrap":'o'}

fig, ax = plt.subplots()
ax = sns.scatterplot(data=penguins_df, x=selected_x_var,
                     y=selected_y_var, hue="вид", 
                     markers=markers, style="вид")

plt.xlabel(selected_x_var)
plt.ylabel(selected_y_var)
plt.title("Диаграмма рассеяния для набора Пингвины Палмера")
st.pyplot(fig)