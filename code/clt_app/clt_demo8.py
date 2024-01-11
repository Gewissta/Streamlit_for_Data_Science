import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Иллюстрация центральной предельной "
         "теоремы с помощью Streamlit")

st.subheader("Приложение Тайлера Ричардса")

st.write(("Это приложение имитирует 1000 подбрасываний монеты, "
          "используя вероятность выпадения «орла», заданную ниже, " 
          "сохраняет результаты в список binom_dist (список binom_dist "
          "выполняет роль генеральной совокупности). Затем из " 
          "этого списка отбирает с возвращением 100 значений, "
          "вычисляет среднее значение и сохраняет его в списке "
          "list_of_means. Приложение делает это 1000 раз и на основе "
          "списка list_of_means строит гистограмму средних значений " 
          "выборок, чтобы проиллюстрировать центральную предельную теорему!"))

perc_heads = st.number_input(
    label="Вероятность выпадения 'орла'", 
     min_value=0.0, max_value=1.0, value=.5)

binom_dist = np.random.binomial(1, perc_heads, 1000)

list_of_means = []
for i in range(0, 1000):
    list_of_means.append(
        np.random.choice(binom_dist, 100, replace=True).mean())

fig, ax = plt.subplots()
ax = plt.hist(list_of_means)
st.pyplot(fig)