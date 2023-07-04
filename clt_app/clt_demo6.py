import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

perc_heads = st.number_input(
    label="Вероятность выпадения 'орла'", 
    min_value=0.0, max_value=1.0, value=.5
)

binom_dist = np.random.binomial(1, perc_heads, 1000)

list_of_means = []
for i in range(0, 1000):
    list_of_means.append(
        np.random.choice(binom_dist, 100, replace=True).mean())
    
fig, ax = plt.subplots()
ax = plt.hist(list_of_means, range=[0,1])
st.pyplot(fig)