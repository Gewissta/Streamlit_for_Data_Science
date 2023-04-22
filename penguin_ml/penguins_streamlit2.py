import streamlit as st
import pickle

rf_pickle = open('random_forest_penguin.pickle', 'rb')
map_pickle = open('output_penguin.pickle', 'rb')
rfc = pickle.load(rf_pickle)
unique_penguin_mapping = pickle.load(map_pickle)
rf_pickle.close()
map_pickle.close()

island = st.selectbox(
    'Остров проживания пингвинов', 
    options=['Biscoe', 'Dream', 'Torgerson'])
sex = st.selectbox(
    'Пол', options=['Женская особь', 'Мужская особь'])
bill_length = st.number_input('Длина клюва (мм)', min_value=0)
bill_depth = st.number_input('Высота клюва (мм)', min_value=0)
flipper_length = st.number_input('Длина ласт (мм)', min_value=0)
body_mass = st.number_input('Масса тела (г)', min_value=0)

st.write('пользовательские вводы {}'.format(
    [island, sex, bill_length,
     bill_depth, flipper_length, body_mass]))