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
    # Case-insensitive column search to avoid 'NoneType' errors if spelling differs
    factor_cols = [col for col in data.columns if 'factor' in col.lower()]
    kesan_cols = [col for col in data.columns if 'impact' in col.lower()]
    measure_cols = [col for col in data.columns if 'measure' in col.lower()]

    # Safety check: If columns aren't found, stop and alert the user
    if not factor_cols or not kesan_cols:
        st.error("⚠️ Error: Could not find columns containing 'Factor' or 'Measure'.")
        st.write("Available columns in your CSV:", list(data.columns))
        st.stop()

# --- HEADER SECTION ---
st.title("📊 Analysis of Factors and Perceptions of Traffic Congestion")
st.write(
     """
     This visual is to analyze the relationship between the factors causing traffic congestion and its impact on road users, as well as evaluate the effectiveness of the proposed intervention measures by taking into account the influence of the demographic profile of the respondents and differences in area categories at the study location.
      """
    )

    # --- NEW: SUMMARY OVERVIEW (SEBELUM AVERAGE SCORES) ---
st.markdown("---")
with st.container():
     st.subheader("📌 Summary Overview")
        
# Mengira statistik ringkas secara dinamik
      total_respondents = len(data)
# Mencari faktor dengan nilai purata tertinggi
      avg_factors = data[factor_cols].mean()
      top_factor_name = avg_factors.idxmax().replace(' Factor', '').replace(' factor', '')
        
# Mencari impak dengan nilai purata tertinggi
      avg_impacts = data[kesan_cols].mean()
      top_impact_name = avg_impacts.idxmax().replace(' Impact', '').replace(' impact', '')
        
# Paparan Metrik
      col_m1, col_m2, col_m3 = st.columns(3)
      col_m1.metric("Total Respondents", f"{total_respondents}")
      col_m2.metric("Primary Cause", top_factor_name)
      col_m3.metric("Major Impact", top_impact_name)

st.info(f"""
        Analysis of the collected data identifies **{top_factor_name}** as the leading contributor to traffic congestion in the studied areas. 
        This congestion significantly leads to **{top_impact_name}** among road users. 
        The following charts provide a detailed breakdown of these factors by demographic and location.
        """
)
    
    st.markdown("---")

# --- SECTION 1: AVERAGE SCORES ---
st.subheader("1. Average Factor Scores (Overall)")
    
factor_means = data[factor_cols].mean().sort_values(ascending=True).reset_index()
factor_means.columns = ['Factor', 'Average Score']
# Cleaning names for display
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
            barmode='group', orientation='h', title='<b>2. Comparison of Factors by Area Type</b>',
            text_auto='.2f'
        )
        fig2.update_layout(height=700)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Column 'Area Type' not found for Demographic Analysis.")

    st.markdown("---")

# --- SECTION 3: HEATMAP ---
st.subheader("🌡️ Heatmap Analysis")

if 'Status' in data.columns:
        heatmap_df = data.groupby('Status')[factor_cols].mean()
        heatmap_df.columns = [col.replace(' Factor', '') for col in heatmap_df.columns]
fig3 = px.imshow(
            heatmap_df, color_continuous_scale='YlGnBu',
            title='<b>3. Heatmap: Factors by Status</b>', text_auto=".2f", aspect="auto"
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Column 'Status' not found for Heatmap Analysis.")
st.markdown("---")

# --- SECTION 4: RELATIONSHIP ANALYSIS ---
st.subheader("🔗 Relationship Analysis")

c1, c2 = st.columns(2)
with c1:
        f_select = st.selectbox("Select Factor (X):", factor_cols, key="factor_box")
with c2:
        k_select = st.selectbox("Select Impact (Y):", kesan_cols, key="impact_box")

if f_select and k_select:
        f_label = f_select.replace(' Factor', '').replace(' factor', '')
        k_label = k_select.replace(' Impact', '').replace(' impact', '')

fig5 = px.scatter(
            data, x=f_select, y=k_select, trendline="ols", 
            trendline_color_override="red", opacity=0.5,
            title=f"Regression: {f_label} vs {k_label}"
        )
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
