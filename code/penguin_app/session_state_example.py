import streamlit as st

st.title("Генератор моего списка важных дел")

my_todo_list = [
    "Купить продукты", 
    "Изучить Streamlit", 
    "Изучить Python"
]

st.write("Мой текущий список важных дел:", my_todo_list)

new_todo = st.text_input("Что нужно сделать?")

if st.button("Добавьте новый элемент списка дел"):
    st.write("Добавление нового элемента в список")
    my_todo_list.append(new_todo)
    
st.write("Мой новый список дел:", my_todo_list)