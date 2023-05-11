import streamlit as st
import pandas as pd
import numpy as np

st.title('Деревья Сан-Франциско')
st.write('Это приложение анализирует деревья в Сан-Франциско '
         'на основе набора данных, любезно предоставленного '
         'Департаментом общественных работ в Сан-Франциско')
trees_df = pd.read_csv('trees.csv')

df_dbh_grouped = pd.DataFrame(
    trees_df.groupby(['dbh']).count()['tree_id'])
df_dbh_grouped.columns = ['количество деревьев']
st.line_chart(df_dbh_grouped)
df_dbh_grouped['new_col'] = np.random.randn(
    len(df_dbh_grouped)) * 500
st.line_chart(df_dbh_grouped)