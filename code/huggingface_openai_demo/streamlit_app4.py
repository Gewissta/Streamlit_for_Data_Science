import openai
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

st.title("Демонстрация OpenAI")

openai.api_key = st.secrets["OPENAI_API_KEY"]
    
system_message_default = """Вы - полезный помощник по анализу тональности.
Вы всегда оцениваете тональность текста и достоверность
вашего анализа тональности с помощью числа от 0 до 1"""

system_message = st.text_area(
    "Введите системное сообщение, чтобы проинструктировать OpenAI", 
    system_message_default
)
analyze_button = st.button("Проанализировать текст")

if analyze_button:
    messages = [
        {
            "role": "system",
            "content": f"{system_message}",
        },
        {
            "role": "user",
            "content": f"Анализ тональности следующего текста: {text}",
        },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    sentiment = response.choices[0].message["content"].strip()
    st.write(sentiment)