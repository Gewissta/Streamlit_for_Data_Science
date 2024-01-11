import streamlit as st

st.title("Генератор моего списка важных дел")

if "my_todo_list" not in st.session_state:
    st.session_state.my_todo_list = [
        "Купить продукты", 
        "Изучить Streamlit",
        "Изучить Python"
    ]

new_todo = st.text_input("Что нужно сделать?")

if st.button("Добавьте новый элемент списка дел"):
    st.write("Добавление нового элемента в список")
    st.session_state.my_todo_list.append(new_todo)
    
st.write("Мой список важных дел:", 
         st.session_state.my_todo_list)