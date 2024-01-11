import streamlit as st
import pandas as pd
trees_df = pd.read_csv('trees.csv')
owners = st.sidebar.multiselect(
    'Tree Owner Filter', trees_df['caretaker'].unique())

st.title('Деревья Сан-Франциско')
st.write('Это приложение анализирует деревья в Сан-Франциско '
         'на основе набора данных, любезно предоставленного '
         'Департаментом общественных работ в Сан-Франциско. '
         'Гистограмма внизу фильтруется по владельцу дерева.')
st.write('В анализе участвуют деревья, которые принадлежат {}.'.format(owners))

if owners:
    trees_df = trees_df[trees_df['caretaker'].isin(owners)]
df_dbh_grouped = pd.DataFrame(trees_df.groupby(['dbh']).count()
                              ['tree_id'])
df_dbh_grouped.columns = ['tree_count']

st.line_chart(df_dbh_grouped)

trees_df = trees_df.dropna(subset=['longitude', 'latitude'])
trees_df = trees_df.sample(n=1000, replace=True)
st.map(trees_df)