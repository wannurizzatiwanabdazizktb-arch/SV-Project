import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Analysis of Traffic Congestion", layout="wide")

# 2. Data URL
DATA_URL = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/project_dataSV(Fatin).csv"

@st.cache_data
def load_data():
    # Load data directly from GitHub
    df = pd.read_csv(DATA_URL)
    return df

try:
    data = load_data()

    # --- DATA PREPARATION ---
    # Mencari kolum secara automatik berdasarkan kata kunci
    factor_cols = [col for col in data.columns if 'factor' in col.lower()]
    kesan_cols = [col for col in data.columns if 'impact' in col.lower()]
    measure_cols = [col for col in data.columns if 'measure' in col.lower()]

    # Safety check
    if not factor_cols or not measure_cols:
        st.error("⚠️ Error: Could not find columns containing 'Factor' or 'Measure'.")
        st.stop()

    # --- HEADER SECTION ---
    st.title("📊 Analysis of Factors and Perceptions of Traffic Congestion")
    st.write(
        """
        This visual is to analyze the relationship between the factors causing traffic congestion and the effectiveness 
        of proposed intervention measures, taking into account the demographic profile and study location.
        """
    )

    # --- SUMMARY OVERVIEW ---
    st.markdown("---")
    with st.container():
        st.subheader("📌 Summary Overview / Ringkasan Eksekutif")
        
        total_respondents = len(data)
        
        # Top Factor
        avg_factors = data[factor_cols].mean()
        top_factor_name = avg_factors.idxmax().replace(' Factor', '').replace(' factor', '')
        
        # Top Measure (Solution)
        avg_measures = data[measure_cols].mean()
        top_measure_name = avg_measures.idxmax().replace(' Measure', '').replace(' measure', '')
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Total Respondents", f"{total_respondents}")
        col_m2.metric("Primary Cause", top_factor_name)
        col_m3.metric("Top Recommended Solution", top_measure_name)

        st.info(f"""
        **Quick Insight:**
        The primary contributor to congestion is identified as **{top_factor_name}**. 
        To address this, respondents highly recommend **{top_measure_name}** as the most effective intervention measure.
        """)
    
    st.markdown("---")

    # --- SECTION 1: AVERAGE SCORES ---
    st.subheader("1. Average Factor Scores (Overall)")
    
    factor_means = data[factor_cols].mean().sort_values(ascending=True).reset_index()
    factor_means.columns = ['Factor', 'Average Score']
    factor_means['Factor'] = factor_means['Factor'].str.replace(' Factor', '', case=False)

    fig1 = px.bar(
        factor_means, x='Average Score', y='Factor', orientation='h',
        title='<b>Average Factor Scores (Overall)</b>',
        color='Average Score', color_continuous_scale='Viridis', text_auto='.2f'
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # --- SECTION 2: DEMOGRAPHIC COMPARISON ---
    st.subheader("🏙️ Demographic Analysis")
    if 'Area Type' in data.columns:
        melted_data = data.melt(id_vars=['Area Type'], value_vars=factor_cols, var_name='Factor', value_name='Score')
        melted_data['Factor'] = melted_data['Factor'].str.replace(' Factor', '', case=False)
        comparison_data = melted_data.groupby(['Area Type', 'Factor'])['Score'].mean().reset_index()

        fig2 = px.bar(
            comparison_data, x='Score', y='Factor', color='Area Type',
            barmode='group', orientation='h', title='<b>Comparison: Urban vs. Rural Areas</b>',
            text_auto='.2f'
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- SECTION 3: CORRELATION HEATMAP ---
    st.subheader("🌡️ Correlation: Causal Factors vs. Congestion Impacts")
    if kesan_cols:
        corr_matrix = data[factor_cols + kesan_cols].corr()
        subset_corr = corr_matrix.loc[factor_cols, kesan_cols]
        subset_corr.index = [c.replace(' Factor', '') for c in subset_corr.index]
        subset_corr.columns = [c.replace(' Impact', '') for c in subset_corr.columns]

        fig3 = px.imshow(subset_corr, text_auto=".2f", color_continuous_scale='YlGnBu', aspect="auto")
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # --- SECTION 4: RELATIONSHIP ANALYSIS ---
    st.subheader("🔗 Relationship Analysis")
    c1, c2 = st.columns(2)
    with c1:
        f_select = st.selectbox("Select Factor (X):", factor_cols)
    with c2:
        m_select = st.selectbox("Select Measure/Solution (Y):", measure_cols)

    fig5 = px.scatter(data, x=f_select, y=m_select, trendline="ols", trendline_color_override="red", opacity=0.5)
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    # --- SECTION 5: SUMMARY CHARTS (FACTOR vs MEASURE) ---
    st.subheader("💡 Summary: Main Causes vs. Solution Steps")

    col_a, col_b = st.columns(2)
    
    with col_a:
        f_plot = data[factor_cols].mean().sort_values(ascending=True).reset_index()
        f_plot.columns = ['Factor', 'Score']
        f_plot['Factor'] = f_plot['Factor'].str.replace(' Factor', '', case=False)
        fig6 = px.bar(f_plot, x='Score', y='Factor', orientation='h', 
                      title='<b>Main Causes (Factors)</b>', 
                      color_discrete_sequence=['#e74c3c'], text_auto='.2f')
        st.plotly_chart(fig6, use_container_width=True)

    with col_b:
        m_plot = data[measure_cols].mean().sort_values(ascending=True).reset_index()
        m_plot.columns = ['Measure', 'Score']
        m_plot['Measure'] = m_plot['Measure'].str.replace(' Measure', '', case=False)
        fig7 = px.bar(m_plot, x='Score', y='Measure', orientation='h', 
                      title='<b>Main Solutions (Measures)</b>', 
                      color_discrete_sequence=['#2ecc71'], text_auto='.2f')
        st.plotly_chart(fig7, use_container_width=True)

except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
