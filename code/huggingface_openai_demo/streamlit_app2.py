import streamlit as st
from transformers import pipeline

st.title("Демонстрация Hugging Face")
text = st.text_input("Введите текст для анализа")

@st.cache_resource()
def get_model():
    return pipeline("sentiment-analysis")

model = get_model()

if text:
    result = model(text)
    st.write("Sentiment:", result[0]["label"])
    st.write("Confidence:", result[0]["score"])