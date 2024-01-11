import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_plotly_events import plotly_events

st.title("Пример использования Streamlit Plotly Events: Пингвины")
df = pd.read_csv("penguins.csv")

fig = px.scatter(df, 
                 x="длина_клюва_мм", 
                 y="высота_клюва_мм", 
                 symbol="вид")

selected_point = plotly_events(fig, click_event=True)
if len(selected_point) == 0:
    st.stop()

selected_x_value = selected_point[0]["x"]
selected_y_value = selected_point[0]["y"]

df_selected = df[
    (df["длина_клюва_мм"] == selected_x_value)
    & (df["высота_клюва_мм"] == selected_y_value)
]
st.write("Данные для отобранной точки:")
st.dataframe(df_selected)