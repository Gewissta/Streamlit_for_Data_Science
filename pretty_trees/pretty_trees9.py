import streamlit as st
import pandas as pd
import seaborn as sns
import datetime as dt
import matplotlib.pyplot as plt

st.title('Деревья Сан-Франциско')
st.write('Это приложение анализирует деревья в Сан-Франциско '
         'на основе набора данных, любезно предоставленного '
         'Департаментом общественных работ в Сан-Франциско. '
         'Графики и карта фильтруются по владельцу дерева.')

trees_df = pd.read_csv('trees.csv')
trees_df['age'] = (pd.to_datetime('today') - pd.to_datetime(
    trees_df['date'])).dt.days

owners = st.sidebar.multiselect('Отбор по владельцу дерева', 
                                trees_df['caretaker'].unique())
if owners:
    trees_df = trees_df[trees_df['caretaker'].isin(owners)]
    
df_dbh_grouped = pd.DataFrame(trees_df.groupby(['dbh']).count()
                              ['tree_id'])
df_dbh_grouped.columns = ['tree_count']

# задаем несколько колонок, добавляем два графика
col1, col2 = st.beta_columns(2)

with col1:
    st.write('Распределение деревьев по диаметру на высоте груди')
    fig_1, ax_1 = plt.subplots()
    ax_1 = sns.histplot(trees_df['dbh'])
    plt.xlabel('Диаметр дерева на высоте груди')
    st.pyplot(fig_1)

with col2:
    st.write('Распределение деревьев по возрасту')
    fig_2, ax_2 = plt.subplots()
    ax_2 = sns.histplot(trees_df['age'])
    plt.xlabel('Возраст (дни)')
    st.pyplot(fig_2)
    
st.write('Распределение деревьев по месторасположению')
trees_df = trees_df.dropna(subset=['longitude', 'latitude'])
trees_df = trees_df.sample(n=1000, replace=True)
st.map(trees_df)