import snowflake.connector
import streamlit as st

@st.cache_resource
def initialize_snowflake_connection():
    session = snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )
    return session

session = initialize_snowflake_connection()

sql_query = """
    SELECT
    l_returnflag,
    sum(l_quantity) as sum_qty,
    sum(l_extendedprice) as sum_base_price
    FROM
    snowflake_sample_data.tpch_sf1.lineitem
    WHERE
    l_shipdate <= dateadd(day, -90, to_date('1998-12-01'))
    GROUP BY 1
"""

st.write("Snowflake Query Result")
df = session.cursor().execute(sql_query).fetch_pandas_all()
st.write(df)