import streamlit as st
import pandas as pd
import seaborn as sns
import datetime as dt
import matplotlib.pyplot as plt

st.title('Деревья Сан-Франциско')
st.write('Это приложение анализирует деревья в Сан-Франциско '
         'на основе набора данных, любезно предоставленного '
         'Департаментом общественных работ в Сан-Франциско. '
         'Гистограммы и карта внизу фильтруются по владельцу дерева.')

# загружаем набор с деревьями, добавляем столбец age
trees_df = pd.read_csv('trees.csv')
trees_df['age'] = (pd.to_datetime('today') -
                   pd.to_datetime(trees_df['date'])).dt.days
# добавляем фильтрацию по типу владельца в боковую 
# панель, затем фильтруем, получаем цвет
owners = st.sidebar.multiselect(
    'Отбор по типу владельца', trees_df['caretaker'].unique())
graph_color = st.sidebar.color_picker('Выбор цвета')
if owners:
    trees_df = trees_df[trees_df['caretaker'].isin(owners)]

# группируем данные по dbh для левого графика
df_dbh_grouped = pd.DataFrame(trees_df.groupby(['dbh']).count()
                              ['tree_id'])
df_dbh_grouped.columns = ['tree_count']

# задаем несколько колонок, добавляем два графика
col1, col2 = st.columns(2)

with col1:
    st.write('Распределение деревьев по диаметру на высоте груди')
    fig_1, ax_1 = plt.subplots()
    ax_1 = sns.histplot(trees_df['dbh'],
                        color=graph_color)
    plt.xlabel('Диаметр дерева на высоте груди')
    st.pyplot(fig_1)
    
with col2:
    st.write('Распределение деревьев по возрасту')
    fig_2, ax_2 = plt.subplots()
    ax_2 = sns.histplot(trees_df['age'],
                        color=graph_color)
    plt.xlabel('Возраст (дни)')
    st.pyplot(fig_2)