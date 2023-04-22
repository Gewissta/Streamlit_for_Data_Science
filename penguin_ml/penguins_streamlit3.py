import streamlit as st
import pickle

st.title('Классификатор пингвинов')
st.write("Это приложение использует 6 признаков для "
         "прогнозирования вида пингвина с помощью "
         "модели случайного леса, обученной на наборе "
         "Пингвины Палмера. Используйте для заполнения "
         "формы ниже!")
         
rf_pickle = open('random_forest_penguin.pickle', 'rb')
map_pickle = open('output_penguin.pickle', 'rb')
rfc = pickle.load(rf_pickle)
unique_penguin_mapping = pickle.load(map_pickle)
rf_pickle.close()
map_pickle.close()

island = st.selectbox('Остров проживания пингвинов', options=[
    'Biscoe', 'Dream', 'Torgerson'])
sex = st.selectbox('Пол', options=['Женская особь', 'Мужская особь'])
bill_length = st.number_input('Длина клюва (мм)', min_value=0)
bill_depth = st.number_input('Высота клюва (мм)', min_value=0)
flipper_length = st.number_input('Длина ласт (мм)', min_value=0)
body_mass = st.number_input('Масса тела (г)', min_value=0)
island_biscoe, island_dream, island_torgerson = 0, 0, 0
if island == 'Biscoe':
    island_biscoe = 1
elif island == 'Dream':
    island_dream = 1
elif island == 'Torgerson':
    island_torgerson = 1
sex_female, sex_male = 0, 0
if sex == 'Женская особь':
    sex_female = 1
elif sex == 'Мужская особь':
    sex_male = 1
    
new_prediction = rfc.predict([[bill_length, bill_depth,
                               flipper_length, body_mass,
                               island_biscoe, island_dream,
                               island_torgerson, sex_female,
                               sex_male]])
prediction_species = unique_penguin_mapping[new_prediction][0]
st.write('Мы прогнозируем, что ваш пингвин относится к виду {}'.format(
    prediction_species))