import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Analysis of Traffic Congestion", layout="wide")

# 2. URL Data
DATA_URL = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/main/project_dataSV_data.csv"

@st.cache_data
def load_data():
    # Menggunakan encoding utf-8 untuk mengelakkan isu karakter
    df = pd.read_csv(DATA_URL)
    return df

try:
    data = load_data()

    # --- PERSEDIAAN DATA ---
    factor_cols = [col for col in data.columns if col.startswith('Faktor')]
    kesan_cols = [col for col in data.columns if col.startswith('Kesan')]
    langkah_cols = [col for col in data.columns if col.startswith('Langkah')]

    # --- BAHAGIAN 1: PURATA SKOR ---
    st.title("📊 Analysis of Factors and Perceptions of Traffic Congestion")
    st.write(
        """
        This visual analysis reveals the main causes of congestion at schools through demographic and status comparisons. 
        Through heatmaps and regression models, we can see how environmental factors influence traffic flow.
        """
    )
    
    factor_means = data[factor_cols].mean().sort_values(ascending=True).reset_index()
    factor_means.columns = ['Factor', 'Average Score']
    factor_means['Factor'] = factor_means['Factor'].str.replace('Faktor ', '')

    fig1 = px.bar(
        factor_means, x='Average Score', y='Factor', orientation='h',
        title='<b>1. Average Factor Scores (Overall)</b>',
        color='Average Score', color_continuous_scale='Viridis', text_auto='.2f'
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # --- BAHAGIAN 2: PERBANDINGAN DEMOGRAFI ---
    st.subheader("🏙️ Demographic Analysis")

    melted_data = data.melt(id_vars=['Jenis Kawasan'], value_vars=factor_cols, var_name='Factor', value_name='Average Score')
    melted_data['Factor'] = melted_data['Factor'].str.replace('Faktor ', '')
    comparison_data = melted_data.groupby(['Jenis Kawasan', 'Factor'])['Average Score'].mean().reset_index()

    fig2 = px.bar(
        comparison_data, x='Average Score', y='Factor', color='Jenis Kawasan',
        barmode='group', orientation='h', title='<b>2. Comparison: Urban vs. Rural Areas</b>',
        text_auto='.2f'
    )
    fig2.update_layout(height=700)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- BAHAGIAN 3: HEATMAP ---
    st.subheader("🌡️ Heatmap Analysis")

    heatmap_df = data.groupby('Status')[factor_cols].mean()
    heatmap_df.columns = [col.replace('Faktor ', '') for col in heatmap_df.columns]

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
        k_select = st.selectbox("Select Impact (Y):", kesan_cols)

    # Pastikan statsmodels telah dipasang: pip install statsmodels
    fig5 = px.scatter(
        data, x=f_select, y=k_select, trendline="ols", 
        trendline_color_override="red", opacity=0.5,
        title=f"Regression: {f_select.replace('Faktor ','')} vs {k_select.replace('Kesan ','')}"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    # --- BAHAGIAN 5: PUNCA VS LANGKAH ---
    st.subheader("💡 Summary: Main Causes vs. Solutions")

    col_a, col_b = st.columns(2)
    
    with col_a:
        f_plot = data[factor_cols].mean().sort_values(ascending=True).reset_index()
        f_plot.columns = ['Factor', 'Score']
        f_plot['Factor'] = f_plot['Factor'].str.replace('Faktor ', '')
        fig6 = px.bar(f_plot, x='Score', y='Factor', orientation='h', title='<b>Main Causes</b>', color_discrete_sequence=['#e74c3c'], text_auto='.2f')
        st.plotly_chart(fig6, use_container_width=True)

    with col_b:
        l_plot = data[langkah_cols].mean().sort_values(ascending=True).reset_index()
        l_plot.columns = ['Measure', 'Score']
        l_plot['Measure'] = l_plot['Measure'].str.replace('Langkah ', '')
        fig7 = px.bar(l_plot, x='Score', y='Measure', orientation='h', title='<b>Most Agreed Solutions</b>', color_discrete_sequence=['#2ecc71'], text_auto='.2f')
        st.plotly_chart(fig7, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data or processing: {e}")
