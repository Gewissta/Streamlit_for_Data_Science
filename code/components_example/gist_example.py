import streamlit as st
from streamlit_embedcode import github_gist

st.title("Пример с Github Gist'ом")
st.write("Код из Streamlit-приложения Пингвины Палмера.")
github_gist('https://gist.github.com/' +
            'Gewissta/859629143a3a8325183b14fefb8eb424')