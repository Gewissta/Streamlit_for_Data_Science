import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_penguin = load_lottieurl(
    "https://assets9.lottiefiles.com/private_files/lf30_lntyk83o.json"
)

st_lottie(lottie_penguin, speed=1.5, width=800, height=400)

st.title("Пингвины Палмера")
st.markdown(
    "Используйте это приложение Streamlit, чтобы создать " 
    "собственную диаграмму рассеяния на основе данных о пингвинах!")

selected_x_var = st.selectbox(
    "Какую переменную отложить по оси x?",
    ["длина_клюва_мм", "высота_клюва_мм", 
     "длина_ласт_мм", "масса_тела_г"])

selected_y_var = st.selectbox(
    "Какую переменную отложить по оси y?",
    ["длина_клюва_мм", "высота_клюва_мм", 
     "длина_ласт_мм", "масса_тела_г"])

penguin_file = st.file_uploader(
    "Выберите CSV-файл с данными о пингвинах")

if penguin_file is not None:
    penguins_df = pd.read_csv(penguin_file)
else:
    penguins_df = pd.read_csv('penguins.csv')

sns.set_style('darkgrid')
markers = {"Adelie": "X", "Gentoo": "s", "Chinstrap":'o'}
fig, ax = plt.subplots()
ax = sns.scatterplot(data=penguins_df, x=selected_x_var,
                     y=selected_y_var, hue='вид', 
                     markers=markers, style='вид')
plt.xlabel(selected_x_var)
plt.ylabel(selected_y_var)
plt.title("Диаграмма рассеяния для набора Пингвины Палмера")
st.pyplot(fig)

st.title("Результат Pandas Profiling для набора Пингвины Палмера")
penguin_profile = ProfileReport(penguins_df, explorative=True)
st_profile_report(penguin_profile)