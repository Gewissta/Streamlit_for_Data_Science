import time

import numpy as np
import streamlit as st

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(50, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Виджеты Streamlit автоматически запускают скрипт сверху вниз. Поскольку
# эта кнопка не связана ни с какой другой логикой, она просто вызывает
# простой повтор.
st.button("Re-run")
