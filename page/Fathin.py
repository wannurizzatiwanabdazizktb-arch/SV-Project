import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Analysis of Traffic Congestion", layout="wide")

# 2. URL Data
DATA_URL = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/cleaned_data%20(Izzati).csv"

@st.cache_data
def load_data():
    # Membaca data
    df = pd.read_csv(DATA_URL)
    
    # --- PEMBERSIHAN HEADER (Penting untuk elak KeyError) ---
    # Membuang ruang kosong di awal/akhir nama kolum
    df.columns = df.columns.str.strip()
    
    # Memastikan kolum kategori dibersihkan kandungannya
    for col in ['Jenis Kawasan', 'Status']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    return df

try:
    data = load_data()

    # --- PERSEDIAAN DATA ---
    factor_cols = [col for col in data.columns if col.startswith('Faktor')]
    kesan_cols = [col for col in data.columns if col.startswith('Kesan')]
    langkah_cols = [col for col in data.columns if col.startswith('Langkah')]

    # Mengira purata faktor awal untuk metrik
    factor_means = data[factor_cols].mean().sort_values(ascending=True).reset_index()
    factor_means.columns = ['Factor', 'Average Score']
    factor_means['Factor'] = factor_means['Factor'].str.replace('Faktor ', '')

    # --- BAHAGIAN 1: HEADER & KPI ---
    st.title("📊 Analysis of Factors and Perceptions of Traffic Congestion")
    st.write(
        """
        This visual analysis reveals the main causes of congestion at schools through demographic and status comparisons. 
        Through heatmaps and regression models, we can see how environmental factors influence traffic flow, 
        helping to design more effective data-driven solutions.
        """
    )

    st.markdown("---")

    # METRIC CARDS (KPIs)
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.metric(label="Total Respondents", value=len(data))
    
    with m2:
        top_factor = factor_means.iloc[-1]['Factor']
        top_score = factor_means.iloc[-1]['Average Score']
        st.metric(label="Top Impact Factor", value=top_factor, delta=f"{top_score:.2f} avg")
    
    with m3:
        if 'Jenis Kawasan' in data.columns:
            melted_temp = data.melt(id_vars=['Jenis Kawasan'], value_vars=factor_cols)
            top_area = melted_temp.groupby('Jenis Kawasan')['value'].mean().idxmax()
            st.metric(label="Most Affected Area", value=top_area)
        else:
            st.metric(label="Area Data", value="Not Found")

    st.markdown("---")

    # --- BAHAGIAN 2: CARTA BAR UTAMA ---
    st.subheader("📈 Overall Factor Ranking")
    fig1 = px.bar(
        factor_means, x='Average Score', y='Factor', orientation='h',
        title='<b>1. Average Factor Scores (Overall)</b>',
        color='Average Score', color_continuous_scale='Viridis', text_auto='.2f'
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # --- BAHAGIAN 3: PERBANDINGAN DEMOGRAFI & HEATMAP ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🏙️ Urban vs. Rural")
        if 'Jenis Kawasan' in data.columns:
            melted_data = data.melt(id_vars=['Jenis Kawasan'], value_vars=factor_cols, var_name='Factor', value_name='Average Score')
            melted_data['Factor'] = melted_data['Factor'].str.replace('Faktor ', '')
            comparison_data = melted_data.groupby(['Jenis Kawasan', 'Factor'])['Average Score'].mean().reset_index()

            fig2 = px.bar(
                comparison_data, x='Average Score', y='Factor', color='Jenis Kawasan',
                barmode='group', orientation='h', title='<b>Factor Scores by Area</b>',
                text_auto='.2f', color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Column 'Jenis Kawasan' missing for demographic analysis.")

    with col_right:
        st.subheader("🌡️ Heatmap: Status Analysis")
        if 'Status' in data.columns:
            heatmap_df = data.groupby('Status')[factor_cols].mean()
            heatmap_df.columns = [col.replace('Faktor ', '') for col in heatmap_df.columns]

            fig3 = px.imshow(
                heatmap_df, color_continuous_scale='YlGnBu',
                title='<b>Heatmap by Respondent Status</b>', text_auto=".2f", aspect="auto"
            )
            st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # --- BAHAGIAN 4: HUBUNGAN (SCATTER PLOT) ---
    st.subheader("🔗 Relationship Analysis")
    sc1, sc2 = st.columns([1, 3])
    with sc1:
        st.info("Analyze how specific factors correlate with perceived impacts.")
        f_select = st.selectbox("Select Factor (X-Axis):", factor_cols)
        k_select = st.selectbox("Select Impact (Y-Axis):", kesan_cols)

    with sc2:
        fig5 = px.scatter(
            data, x=f_select, y=k_select, trendline="ols", 
            trendline_color_override="red", opacity=0.4,
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
        fig7 = px.bar(l_plot, x='Score', y='Measure', orientation='h', title='<b>Proposed Solutions</b>', color_discrete_sequence=['#2ecc71'], text_auto='.2f')
        st.plotly_chart(fig7, use_container_width=True)

except Exception as e:
    st.error(f"An error occurred: {e}")
    st.info("Check if your CSV column names match the expected names in the code.")
