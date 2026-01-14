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
    df = pd.read_csv(DATA_URL)
    return df

try:
    data = load_data()

    # --- DATA PREPARATION ---
    factor_cols = [col for col in data.columns if 'factor' in col.lower()]
    kesan_cols = [col for col in data.columns if 'impact' in col.lower()]
    measure_cols = [col for col in data.columns if 'measure' in col.lower()]

    if not factor_cols or not kesan_cols:
        st.error("⚠️ Error: Could not find columns containing 'Factor' or 'Impact'.")
        st.write("Available columns:", list(data.columns))
        st.stop()

    # --- HEADER SECTION ---
    st.title("📊 Analysis of Factors and Perceptions of Traffic Congestion")
    st.write("This visual analyzes the relationship between the factor causing traffic congestion and impact on road users...")

    st.markdown("---")

    # --- SUMMARY OVERVIEW ---
    with st.container():
        st.subheader("📌 Summary Overview")
        avg_factors = data[factor_cols].mean()
        top_factor_name = avg_factors.idxmax().replace(' Factor', '').replace(' factor', '')
        avg_impacts = data[kesan_cols].mean()
        top_impact_name = avg_impacts.idxmax().replace(' Impact', '').replace(' impact', '')
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Primary Cause", top_factor_name)
        col_m2.metric("Major Impact", top_impact_name)

    st.info(f"Analysis identifies **{top_factor_name}** as the leading contributor.")
    st.markdown("---")

    # --- SECTION 1: AVERAGE SCORES (IN PERCENTAGE) ---
    st.subheader("1. Average Factor Scores (Percentage)")
    factor_means = data[factor_cols].mean().sort_values(ascending=True).reset_index()
    factor_means.columns = ['Factor', 'Score']
    factor_means['Percentage'] = (factor_means['Score'] / 5) * 100
    factor_means['Factor'] = factor_means['Factor'].str.replace(' Factor', '', case=False)

    fig1 = px.bar(
        factor_means, x='Percentage', y='Factor', orientation='h',
        title='<b>Average Factor Importance (%)</b>',
        color='Percentage', color_continuous_scale='Viridis', text_auto='.1f'
    )
    fig1.update_layout(xaxis_ticksuffix="%")
    st.plotly_chart(fig1, use_container_width=True)
    st.write(f"Factor **{factor_means.iloc[-1]['Factor']}** recorded the highest percentage of **{factor_means.iloc[-1]['Percentage']:.1f}%**.")

    st.markdown("---")

    # --- SECTION 2: DEMOGRAPHIC COMPARISON ---
    st.subheader("City Demographic Analysis")
    if 'Area Type' in data.columns:
        melted_data = data.melt(id_vars=['Area Type'], value_vars=factor_cols, var_name='Factor', value_name='Score')
        # Tukar Score ke Percentage
        melted_data['Percentage'] = (melted_data['Score'] / 5) * 100
        comparison_data = melted_data.groupby(['Area Type', 'Factor'])['Percentage'].mean().reset_index()
        
        fig2 = px.bar(comparison_data, x='Percentage', y='Factor', color='Area Type', barmode='group', orientation='h', text_auto='.1f')
        fig2.update_layout(xaxis_ticksuffix="%")
        st.plotly_chart(fig2, use_container_width=True)
    
    st.write("The graph illustrates the varying perceptions across Urban, Suburban, and Rural areas...")

    st.markdown("---")

    # --- SECTION 3: HEATMAP ---
    st.subheader("🌡️ Heatmap Analysis")
    if 'Status' in data.columns:
        heatmap_df = data.groupby('Status')[factor_cols].mean()
        heatmap_perc = (heatmap_df / 5) * 100
        fig3 = px.imshow(heatmap_perc, text_auto=".1f", aspect="auto", color_continuous_scale='YlGnBu')
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # --- SECTION 4: RELATIONSHIP ---
    st.subheader("🔗 Relationship Analysis")
    c1, c2 = st.columns(2)
    with c1:
        f_select = st.selectbox("Select Factor (X):", factor_cols)
    with c2:
        k_select = st.selectbox("Select Impact (Y):", kesan_cols)
    
    fig5 = px.scatter(data, x=f_select, y=k_select, trendline="ols")
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    # --- SECTION 5: SUMMARY CHARTS (FACTOR vs MEASURE) ---
    st.subheader("💡 Summary: Main Causes vs. Solution Steps")
    col_a, col_b = st.columns(2)
    
    with col_a:
        f_plot = data[factor_cols].mean().sort_values(ascending=True).reset_index()
        f_plot.columns = ['Factor', 'Score']
        f_plot['Percentage'] = (f_plot['Score'] / 5) * 100
        fig6 = px.bar(f_plot, x='Percentage', y='Factor', orientation='h', 
                      title='<b>Main Causes (%)</b>', color_discrete_sequence=['#e74c3c'], text_auto='.1f')
        fig6.update_layout(xaxis_ticksuffix="%")
        st.plotly_chart(fig6, use_container_width=True)

    with col_b:
        m_plot = data[measure_cols].mean().sort_values(ascending=True).reset_index()
        m_plot.columns = ['Measure', 'Score']
        m_plot['Percentage'] = (m_plot['Score'] / 5) * 100
        fig7 = px.bar(m_plot, x='Percentage', y='Measure', orientation='h', 
                      title='<b>Main Solutions (%)</b>', color_discrete_sequence=['#2ecc71'], text_auto='.1f')
        fig7.update_layout(xaxis_ticksuffix="%")
        st.plotly_chart(fig7, use_container_width=True)

except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
