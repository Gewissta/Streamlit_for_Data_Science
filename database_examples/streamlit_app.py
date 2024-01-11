import snowflake.connector
import streamlit as st

session = snowflake.connector.connect(
    **st.secrets["snowflake"], client_session_keep_alive=True
)

sql_query = "select 1"
st.write("Snowflake Query Result")
df = session.cursor().execute(sql_query).fetch_pandas_all()
st.write(df)