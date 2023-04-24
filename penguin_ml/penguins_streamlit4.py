import streamlit as st
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

st.title("Классификатор пингвинов")
st.write("Это приложение использует 6 признаков для "
         "прогнозирования вида пингвина с помощью "
         "модели случайного леса, обученной на наборе "
         "Пингвины Палмера. Используйте для заполнения "
         "форму ниже!")

penguin_file = st.file_uploader(
    "Загрузите ваши данные с характеристиками пингвинов")

if penguin_file is None:
    rf_pickle = open('random_forest_penguin.pickle', 'rb')
    map_pickle = open('output_penguin.pickle', 'rb')
    rfc = pickle.load(rf_pickle)
    unique_penguin_mapping = pickle.load(map_pickle)
    rf_pickle.close()
    map_pickle.close()
else:
    penguin_df = pd.read_csv(penguin_file)
    penguin_df = penguin_df.dropna()
    output = penguin_df['вид']
    features = penguin_df[['остров', 'длина_клюва_мм', 
                           'высота_клюва_мм', 'длина_ласт_мм', 
                           'масса_тела_г', 'пол']]
    
    features = pd.get_dummies(features)
    features.columns = features.columns.str.replace('\s+', '_')
    output, unique_penguin_mapping = pd.factorize(output)
    x_train, x_test, y_train, y_test = train_test_split(
        features, output, test_size=0.8)
    rfc = RandomForestClassifier(random_state=15)
    rfc.fit(x_train, y_train)
    y_pred = rfc.predict(x_test)
    score = round(accuracy_score(y_pred, y_test), 2)
    st.write(
        f"""Мы обучили модель случайного леса на этих данных,
        получили правильность {score}! Используйте поля для
        ввода ниже для апробации модели."""
    )

with st.form("пользовательские вводы"):
    island = st.selectbox("Остров проживания пингвинов", 
                          options=["Biscoe", "Dream", "Torgerson"])
    sex = st.selectbox("Пол", options=["Женская особь", "Мужская особь"])
    bill_length = st.number_input("Длина клюва (мм)", min_value=0)
    bill_depth = st.number_input("Высота клюва (мм)", min_value=0)
    flipper_length = st.number_input("Длина ласт (мм)", min_value=0)
    body_mass = st.number_input("Масса тела (г)", min_value=0)
    st.form_submit_button()
    
island_biscoe, island_dream, island_torgerson = 0, 0, 0
if island == "Biscoe":
    island_biscoe = 1
elif island == "Dream":
    island_dream = 1
elif island == "Torgerson":
    island_torgerson = 1
    
sex_female, sex_male = 0, 0
if sex == "Женская особь":
    sex_female = 1
elif sex == "Мужская особь":
    sex_male = 1
    
new_prediction = rfc.predict([[bill_length, bill_depth,
                               flipper_length, body_mass,
                               island_biscoe, island_dream,
                               island_torgerson, sex_female,
                               sex_male]])
prediction_species = unique_penguin_mapping[new_prediction][0]
st.write("Мы прогнозируем, что ваш пингвин относится к виду {}".format(
    prediction_species))