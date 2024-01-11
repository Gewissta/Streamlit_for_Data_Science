import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

st.title('Деревья Сан-Франциско')
st.write('Это приложение анализирует деревья в Сан-Франциско '
         'на основе набора данных, любезно предоставленного '
         'Департаментом общественных работ в Сан-Франциско')
trees_df = pd.read_csv('trees.csv')
trees_df['age'] = (pd.to_datetime('today') - pd.to_datetime(
    trees_df['date'])).dt.days

st.subheader('График Seaborn')
fig_sb, ax_sb = plt.subplots()
ax_sb = sns.histplot(trees_df['age'])
plt.xlabel('Возраст дерева (в днях)')
st.pyplot(fig_sb)

st.subheader('График Matploblib')
fig_mpl, ax_mpl = plt.subplots()
ax_mpl = plt.hist(trees_df['age'])
plt.xlabel('Возраст дерева (в днях)')
st.pyplot(fig_mpl)