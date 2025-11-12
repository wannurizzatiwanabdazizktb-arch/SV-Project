import streamlit as st
import pandas as pd

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8nPPwgVKnGxpQLQFTH6EQLpO6l1l2BlEAdGqmb0Bq7FGQzViLwKbb78NMjJSA1-eHl-Ebq5Wl4LRU/pub?gid=745446698&single=true&output=csv"
df = pd.read_csv(url)

# Exclude columns by name
df = df.drop(columns=["Timestamp", "Score"])

st.dataframe(df)
