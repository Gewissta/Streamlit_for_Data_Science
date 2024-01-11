import streamlit as st
from transformers import pipeline

st.title("Демонстрация Hugging Face")
text = st.text_input("Введите текст для анализа")
model = pipeline("sentiment-analysis")

if text:
    result = model(text)
    st.write("Sentiment:", result[0]["label"])
    st.write("Confidence:", result[0]["score"])