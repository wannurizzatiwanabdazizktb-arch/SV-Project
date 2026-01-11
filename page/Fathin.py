import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# 1. URL Data & Load Data
# Menggunakan URL data yang anda berikan
DATA_URL = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/cleaned_data%20(Izzati).csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    # Memastikan ruang kosong (spaces) pada nama kolum dibuang
    df.columns = df.columns.str.strip()
    return df

data = load_data()

# 2. Persediaan Kolom
# Kita pastikan hanya kolum yang wujud dan mempunyai prefix yang betul diambil
factor_cols = [col for col in data.columns if col.startswith('Faktor')]
kesan_cols = [col for col in data.columns if col.startswith('Kesan')]
langkah_cols = [col for col in data.columns if col.startswith('Langkah')]

# --- 3. Paparan Header & KPI ---
st.title("📊 Analysis of Factors and Perceptions of Traffic Congestion")

st.markdown("---")
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

with col_kpi1:
    st.metric("Total Respondents", len(data)) 

with col_kpi2:
    # Menggunakan blok try-except atau semakan if untuk mengelakkan ralat idxmax
    if len(factor_cols) > 0:
        # Pastikan kita menukar data kepada numerik sebelum mengira mean
        factor_means = data[factor_cols].apply(pd.to_numeric, errors='coerce').mean()
        
        if not factor_means.isnull().all():
            top_factor_name = factor_means.idxmax()
            top_factor_display = top_factor_name.replace('Faktor ', '')
            st.metric("Main Factor", top_factor_display)
        else:
            st.metric("Main Factor", "No Numeric Data")
    else:
        st.metric("Main Factor", "Column Not Found")

with col_kpi3:
    if len(langkah_cols) > 0:
        # Pastikan data ditukar kepada numerik
        langkah_means = data[langkah_cols].apply(pd.to_numeric, errors='coerce').mean()
        
        if not langkah_means.isnull().all():
            top_measure_name = langkah_means.idxmax()
            top_measure_display = top_measure_name.replace('Langkah ', '')
            st.metric("Top Solution", top_measure_display)
        else:
            st.metric("Top Solution", "No Numeric Data")
    else:
        st.metric("Top Solution", "Column Not Found")

st.markdown("---")

# --- 4. Visualisasi (Contoh Graf Bar) ---
if len(factor_cols) > 0:
    # Kira purata dan susun
    f_means = data[factor_cols].apply(pd.to_numeric, errors='coerce').mean().sort_values(ascending=True).reset_index()
    f_means.columns = ['Factor', 'Average Score']
    f_means['Factor'] = f_means['Factor'].str.replace('Faktor ', '')

    fig1 = px.bar(
        f_means, 
        x='Average Score', 
        y='Factor', 
        orientation='h',
        title='<b>Average Factor Scores (Overall)</b>',
        color='Average Score',
        color_continuous_scale='Viridis',
        text_auto='.2f'
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.error("Data 'Faktor' tidak ditemui. Sila semak format fail CSV anda.")
