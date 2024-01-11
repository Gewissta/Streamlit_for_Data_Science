import pandas as pd
import pydeck as pdk
import streamlit as st

st.title('Деревья Сан-Франциско')
st.write('Это приложение анализирует деревья в Сан-Франциско '
         'на основе набора данных, любезно предоставленного '
         'Департаментом общественных работ в Сан-Франциско')
trees_df = pd.read_csv('trees.csv')
trees_df.dropna(how='any', inplace=True)

sf_initial_view = pdk.ViewState(
    latitude=37.77,
    longitude=-122.4,
    zoom=11,
    pitch=30
)

hx_layer = pdk.Layer(
    'HexagonLayer',
    data = trees_df,
    get_position=['longitude', 'latitude'],
    radius=100,
    extruded=True)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=sf_initial_view,
    layers=[hx_layer]
))