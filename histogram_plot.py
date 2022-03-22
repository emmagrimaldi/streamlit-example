# histogram_plot.py

import streamlit as st
import snowflake.connector
import matplotlib.pyplot as plt
import numpy as np


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
scores_array = np.asarray(rows)

fig = plt.figure(figsize=(16, 16))
n, bins, patches = plt.hist(scores_array, bins=50)
plt.xlabel('Midterm General Score')
plt.title('Histogram of random Scores (N=1,000)')


# Plot!
st.plotly_chart(fig, use_container_width=True)
