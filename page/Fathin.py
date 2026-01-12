import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Analysis of Traffic Congestion", layout="wide")

# 2. URL Data
# Menggunakan URL raw GitHub yang anda berikan
DATA_URL = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/cleaned_data%20(Izzati).csv"

@st.cache_data
def load_data():
    # Load data terus dari GitHub
    df = pd.read_csv(DATA_URL)
    return df

try:
    data = load_data()

    # --- PERSEDIAAN DATA ---
    # Mengenal pasti kolum mengikut kata kunci dalam fail CSV Izzati
    factor_cols = [col for col in data.columns if 'Factor' in col]
    kesan_cols = [col for col in data.columns if 'Effect' in col]

    # --- BAHAGIAN 1: PURATA SKOR ---
    st.title("📊 Analysis of Factors and Perceptions of Traffic Congestion")
    st.write(
        """
        Visual analisis ini mendedahkan punca utama kesesakan melalui perbandingan demografi dan status. 
        Melalui heatmap dan model regresi, kita dapat melihat bagaimana faktor persekitaran mempengaruhi aliran trafik.
        """
    )
    
    factor_means = data[factor_cols].mean().sort_values(ascending=True).reset_index()
    factor_means.columns = ['Factor', 'Average Score']
    # Membersihkan nama kolum untuk paparan (buang perkataan 'Factor')
    factor_means['Factor'] = factor_means['Factor'].str.replace(' Factor', '')

    fig1 = px.bar(
        factor_means, x='Average Score', y='Factor', orientation='h',
        title='<b>1. Average Factor Scores (Overall)</b>',
        color='Average Score', color_continuous_scale='Viridis', text_auto='.2f'
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # --- BAHAGIAN 2: PERBANDINGAN DEMOGRAFI ---
    st.subheader("🏙️ Demographic Analysis")

    melted_data = data.melt(id_vars=['Area Type'], value_vars=factor_cols, var_name='Factor', value_name='Score')
    melted_data['Factor'] = melted_data['Factor'].str.replace(' Factor', '')
    comparison_data = melted_data.groupby(['Area Type', 'Factor'])['Score'].mean().reset_index()

    fig2 = px.bar(
        comparison_data, x='Score', y='Factor', color='Area Type',
        barmode='group', orientation='h', title='<b>2. Comparison: Urban vs. Rural Areas</b>',
        text_auto='.2f'
    )
    fig2.update_layout(height=700)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- BAHAGIAN 3: HEATMAP ---
    st.subheader("🌡️ Heatmap Analysis")

    # Menggunakan 'Status' sebagai paksi Y untuk heatmap
    heatmap_df = data.groupby('Status')[factor_cols].mean()
    heatmap_df.columns = [col.replace(' Factor', '') for col in heatmap_df.columns]

    fig3 = px.imshow(
        heatmap_df, color_continuous_scale='YlGnBu',
        title='<b>3. Heatmap: Factors by Status</b>', text_auto=".2f", aspect="auto"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # --- BAHAGIAN 4: HUBUNGAN (SCATTER PLOT) ---
    st.subheader("🔗 Relationship Analysis")

    c1, c2 = st.columns(2)
    with c1:
        f_select = st.selectbox("Select Factor (X):", factor_cols)
    with c2:
        k_select = st.selectbox("Select Effect (Y):", kesan_cols)

    # Pastikan statsmodels telah dipasang: pip install statsmodels
    fig5 = px.scatter(
        data, x=f_select, y=k_select, trendline="ols", 
        trendline_color_override="red", opacity=0.5,
        title=f"Regression: {f_select.replace(' Factor','')} vs {k_select.replace(' Effect','')}"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    # --- BAHAGIAN 5: PUNCA VS KESAN ---
    st.subheader("💡 Summary: Main Causes vs. Effects")

    col_a, col_b = st.columns(2)
    
    with col_a:
        f_plot = data[factor_cols].mean().sort_values(ascending=True).reset_index()
        f_plot.columns = ['Factor', 'Score']
        f_plot['Factor'] = f_plot['Factor'].str.replace(' Factor', '')
        fig6 = px.bar(f_plot, x='Score', y='Factor', orientation='h', title='<b>Main Causes (Factors)</b>', color_discrete_sequence=['#e74c3c'], text_auto='.2f')
        st.plotly_chart(fig6, use_container_width=True)

    with col_b:
        e_plot = data[kesan_cols].mean().sort_values(ascending=True).reset_index()
        e_plot.columns = ['Effect', 'Score']
        e_plot['Effect'] = e_plot['Effect'].str.replace(' Effect', '')
        fig7 = px.bar(e_plot, x='Score', y='Effect', orientation='h', title='<b>Main Impacts (Effects)</b>', color_discrete_sequence=['#f39c12'], text_auto='.2f')
        st.plotly_chart(fig7, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data or processing: {e}")
