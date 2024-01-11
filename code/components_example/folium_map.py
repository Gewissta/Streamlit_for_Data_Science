import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

st.title("Деревья Сан-Франциско")

trees_df = pd.read_csv("trees.csv")
trees_df = trees_df.dropna(subset=["longitude", "latitude"])
trees_df = trees_df.head(n=100)
lat_avg = trees_df["latitude"].mean()
lon_avg = trees_df["longitude"].mean()
m = folium.Map(location=[lat_avg, lon_avg], zoom_start=12)
st_folium(m)