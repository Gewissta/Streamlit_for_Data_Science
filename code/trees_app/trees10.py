import pandas as pd
import pydeck as pdk
import streamlit as st

st.title('Деревья Сан-Франциско')
st.write('Это приложение анализирует деревья в Сан-Франциско '
         'на основе набора данных, любезно предоставленного '
         'Департаментом общественных работ в Сан-Франциско')
trees_df = pd.read_csv('trees.csv')

sf_initial_view = pdk.ViewState(
    latitude=37.77,
    longitude=-122.4
)

st.pydeck_chart(pdk.Deck(
    initial_view_state=sf_initial_view
))