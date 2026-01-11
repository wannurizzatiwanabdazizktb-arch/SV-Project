import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# 1. Page Configuration (Mesti baris pertama selepas import)
# Nota: Jika fail ini dipanggil melalui st.navigation, set_page_config mungkin tidak diperlukan di sini 
# bergantung pada cara main file anda disusun.

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

# --- 🟢 LANGKAH PENTING: Takrifkan filtered_data di sini ---
st.sidebar.header("Dashboard Filters")
selected_status = st.sidebar.multiselect("Select Status:", options=data['Status'].unique(), default=data['Status'].unique())
selected_area = st.sidebar.multiselect("Select Area Type:", options=data['Jenis Kawasan'].unique(), default=data['Jenis Kawasan'].unique())

# Baris ini MESTI ada sebelum st.metric dipanggil
filtered_data = data[(data['Status'].isin(selected_status)) & (data['Jenis Kawasan'].isin(selected_area))]

# --- 4. Paparan Header & KPI ---
st.title("📊 Analysis of Factors and Perceptions of Traffic Congestion")

st.markdown("---")
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
with col_kpi1:
    # Sekarang filtered_data sudah wujud, ralat baris 38 akan hilang
    st.metric("Total Respondents", len(filtered_data)) 

with col_kpi2:
    if not filtered_data.empty:
        top_factor = filtered_data[factor_cols].mean().idxmax().replace('Faktor ', '')
        st.metric("Main Factor", top_factor)
    else:
        st.metric("Main Factor", "N/A")

with col_kpi3:
    if not filtered_data.empty:
        top_measure = filtered_data[langkah_cols].mean().idxmax().replace('Langkah ', '')
        st.metric("Top Solution", top_measure)
    else:
        st.metric("Top Solution", "N/A")
st.markdown("---")

# Teruskan dengan baki kod graf anda menggunakan 'filtered_data'...
