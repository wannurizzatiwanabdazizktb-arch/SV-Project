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
    st.write("This visual analyzes factors causing traffic congestion and its impact on road users.")

    st.markdown("---")

    # --- SUMMARY OVERVIEW ---
    with st.container():
        st.subheader("📌 Summary Overview")
        total_respondents = len(data)
        
        avg_factors = data[factor_cols].mean()
        top_factor_name = avg_factors.idxmax().replace(' Factor', '').replace(' factor', '')
        
        avg_impacts = data[kesan_cols].mean()
        top_impact_name = avg_impacts.idxmax().replace(' Impact', '').replace(' impact', '')
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Total Respondents", f"{total_respondents}")
        col_m2.metric("Primary Cause", top_factor_name)
        col_m3.metric("Major Impact", top_impact_name)

    st.info(f"Analysis identifies **{top_factor_name}** as the leading contributor.")
    st.markdown("---")

    # --- SECTION 1: AVERAGE SCORES ---
    st.subheader("1. Average Factor Scores (Overall)")
    factor_means = data[factor_cols].mean().sort_values(ascending=True).reset_index()
    factor_means.columns = ['Factor', 'Average Score']
    factor_means['Factor'] = factor_means['Factor'].str.replace(' Factor', '', case=False)

    fig1 = px.bar(
        factor_means, x='Average Score', y='Factor', orientation='h',
        title='Average Factor Scores', color='Average Score', text_auto='.2f'
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # FIXED: Added the missing closing parenthesis below
    st.write("This graph shows that infrastructure issues are the main cause of the problem compared to behavioral factors.")

    st.markdown("---")

    # --- SECTION 2: DEMOGRAPHIC COMPARISON ---
    st.subheader("City Demographic Analysis")
    if 'Area Type' in data.columns:
        melted_data = data.melt(id_vars=['Area Type'], value_vars=factor_cols, var_name='Factor', value_name='Score')
        comparison_data = melted_data.groupby(['Area Type', 'Factor'])['Score'].mean().reset_index()
        fig2 = px.bar(comparison_data, x='Score', y='Factor', color='Area Type', barmode='group', orientation='h')
        st.plotly_chart(fig2, use_container_width=True)

    st.write("This graph shows that rural areas experience the most significant impact of almost all of the disruption factors studied, especially infrastructure issues such as lack of parking and narrow roads, while student car sharing practices are the factor with the lowest impact across all area categories.")

    st.markdown("---")

    # --- SECTION 3: HEATMAP ---
    st.subheader("🌡️ Heatmap Analysis")
    if 'Status' in data.columns:
        heatmap_df = data.groupby('Status')[factor_cols].mean()
        fig3 = px.imshow(heatmap_df, text_auto=".2f", aspect="auto")
        st.plotly_chart(fig3, use_container_width=True)

    st.write("This heatmap graph shows that university students are the group that gives the highest scores on most factors, with the issue of lack of parking being the most critical problem for them and their parents.")

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
    st.write("This Regression Graph shows the relationship between factors and effects and for example there is a positive relationship between rainy weather and the impact of accidents, which shows that an increase in adverse weather factors contributes directly to an increase in the risk of accidents.")

    st.markdown("---")
    
# --- SECTION 5: SUMMARY CHARTS ---
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
        st.write("This graph shows that lack of parking spaces and road damage are the main factors of traffic disruption. To overcome this issue, respondents suggested the implementation of special drop-off zones and traffic officers as effective solutions.")

except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
