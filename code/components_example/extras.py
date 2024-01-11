import streamlit as st
from streamlit_extras.mandatory_date_range import date_range_picker
result = date_range_picker("Выберите диапазон дат")
st.write("Результат:", result)

from streamlit_extras.stoggle import stoggle

stoggle(
    "Щелкни меня!",
    """🥷 Сюрприз! Здесь дополнительный контент""",
)