import streamlit as st
import pandas as pd

st.title('Деревья Сан-Франциско')
st.write('Это приложение анализирует деревья в Сан-Франциско '
         'на основе набора данных, любезно предоставленного '
         'Департаментом общественных работ в Сан-Франциско')
trees_df = pd.read_csv('trees.csv')

df_dbh_grouped = pd.DataFrame(trees_df.groupby(['dbh']).count()
                              ['tree_id'])
df_dbh_grouped.columns = ['tree_count']
col1, col2, col3 = st.beta_columns(3)

with col1:
    st.line_chart(df_dbh_grouped)
with col2:
    st.bar_chart(df_dbh_grouped)
with col3:
    st.area_chart(df_dbh_grouped)