import pandas as pd
pd.set_option('display.max_columns', 20)

from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

import pickle

penguin_df = pd.read_csv('penguins.csv')
penguin_df.dropna(inplace=True)
output = penguin_df['вид']
features = penguin_df[['остров', 'длина_клюва_мм', 
                       'высота_клюва_мм', 'длина_ласт_мм', 
                       'масса_тела_г', 'пол']]
features = pd.get_dummies(features)
features.columns = features.columns.str.replace('\s+', '_')
print(features.columns.tolist())
print("")
print(features.head())
output, uniques = pd.factorize(output)

x_train, x_test, y_train, y_test = train_test_split(
    features, output, test_size=.8)
rfc = RandomForestClassifier(random_state=15)
rfc.fit(x_train, y_train)
y_pred = rfc.predict(x_test)
score = accuracy_score(y_pred, y_test)
print("\nПравильность нашей модели равна {}".format(score))

rf_pickle = open('random_forest_penguin.pickle', 'wb')
pickle.dump(rfc, rf_pickle)
rf_pickle.close()
output_pickle = open('output_penguin.pickle', 'wb')
pickle.dump(uniques, output_pickle)
output_pickle.close()