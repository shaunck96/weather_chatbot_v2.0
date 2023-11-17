import streamlit as st
import psycopg2
import pandas as pd


@st.cache_resource(ttl=600)
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()


@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * FROM public.current_weather")
columns = run_query("Select * FROM public.current_weather LIMIT 0")
colnames = [desc[0] for desc in conn.cursor.description]
data = pd.DataFrame(rows)
data.columns = colnames
st.table(data)

