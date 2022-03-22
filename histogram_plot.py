# histogram_plot.py

import streamlit as st
import snowflake.connector
import matplotlib.pyplot as plt


# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])


conn = init_connection()


# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


rows = run_query("SELECT ts_tsmart_midterm_general_turnout_score FROM targetsmart_archive.tsdata_2022_02 limit 1000;")

fig = plt.figure(figsize=(16,  6))
n, bins, patches = plt.hist(rows['ts_tsmart_midterm_general_turnout_score'])
