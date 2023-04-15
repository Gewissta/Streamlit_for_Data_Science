import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

binom_dist = np.random.binomial(1, .5, 1000)
list_of_means = []
for i in range(0, 1000):
    list_of_means.append(
        np.random.choice(binom_dist, 100, replace=True).mean())
    
plt.hist(list_of_means)
st.pyplot()
plt.hist([1,1,1,1])
st.pyplot()