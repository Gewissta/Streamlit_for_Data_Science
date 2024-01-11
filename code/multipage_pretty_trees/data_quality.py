import pandas as pd
import streamlit as st

st.title("Приложение Качество данных Деревья Сан-Франциско")
st.write(
    """
    Это приложение представляет собой инструмент редактирования 
    набора данных деревьев SF. Отредактируйте данные 
    и сохраните в новый файл!
    """
)
trees_df = pd.read_csv("trees.csv")
trees_df = trees_df.dropna(subset=["longitude", "latitude"])
trees_df_filtered = trees_df[trees_df["legal_status"] == "Private"]
edited_df = st.data_editor(trees_df_filtered)