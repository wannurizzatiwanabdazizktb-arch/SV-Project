import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# 1. Page Configuration
# Nota: Kekalkan jika fail ini adalah fail utama, buang jika dipanggil oleh st.navigation
# st.set_page_config(page_title="Traffic Congestion Analysis", layout="wide")

# 2. URL Data & Load Data
DATA_URL = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/cleaned_data%20(Izzati).csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    return df

data = load_data()

# 3. Persediaan Kolom
factor_cols = [col for col in data.columns if col.startswith('Faktor')]
kesan_cols = [col for col in data.columns if col.startswith('Kesan')]
langkah_cols = [col for col in data.columns if col.startswith('Langkah')]

# --- 4. Paparan Header & KPI ---
st.title("📊 Analysis of Factors and Perceptions of Traffic Congestion")

st.markdown("---")
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

# Menggunakan 'data' secara terus kerana filter telah dibuang
with col_kpi1:
    st.metric("Total Respondents", len(data)) 

with col_kpi2:
    if not data.empty:
        # Mencari min daripada keseluruhan data
        top_factor = data[factor_cols].mean().idxmax().replace('Faktor ', '')
        st.metric("Main Factor", top_factor)
    else:
        st.metric("Main Factor", "N/A")

with col_kpi3:
    if not data.empty:
        # Mencari min daripada keseluruhan data
        top_measure = data[langkah_cols].mean().idxmax().replace('Langkah ', '')
        st.metric("Top Solution", top_measure)
    else:
        st.metric("Top Solution", "N/A")

st.markdown("---")

# --- CONTOH GRAF MENGGUNAKAN DATA KESELURUHAN ---
# Pastikan setiap graf selepas ini menggunakan pembolehubah 'data'
factor_means = data[factor_cols].mean().sort_values(ascending=True).reset_index()
factor_means.columns = ['Factor', 'Average Score']
factor_means['Factor'] = factor_means['Factor'].str.replace('Faktor ', '')

fig1 = px.bar(
    factor_means, 
    x='Average Score', 
    y='Factor', 
    orientation='h',
    title='<b>Average Factor Scores (Overall)</b>',
    color='Average Score',
    color_continuous_scale='Viridis',
    text_auto='.2f'
)
st.plotly_chart(fig1, use_container_width=True)
