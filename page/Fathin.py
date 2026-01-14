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
    st.write("This visual analyzes the relationship between the factor causing traffic congestion and impact on road users as weel as evaluate the effectiveness of the proposed intervention measure by taking into the influence of the demographic profile of the respondent and differences in area categories at the study location.")

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

# 1. Kira purata asal
factor_means = data[factor_cols].mean().sort_values(ascending=True).reset_index()
factor_means.columns = ['Factor', 'Score']

# 2. Formula Tukar ke Peratus: (Skor / 5) * 100
# Anda boleh tukar angka 5 kepada 4 atau 7 mengikut skala maksimum anda
factor_means['Percentage'] = (factor_means['Score'] / 5) * 100

# 3. Bersihkan nama untuk paparan
factor_means['Factor'] = factor_means['Factor'].str.replace(' Factor', '', case=False)

# 4. Bina Grafik
fig1 = px.bar(
    factor_means, 
    x='Percentage', 
    y='Factor', 
    orientation='h',
    title='<b>Average Factor Importance (%)</b>',
    color='Percentage', 
    color_continuous_scale='Viridis',
    text_auto='.1f', # Papar 1 tempat perpuluhan
    labels={'Percentage': 'Importance (%)'}
)

# Tambah simbol '%' pada label paksi X
fig1.update_layout(xaxis_ticksuffix="%")

st.plotly_chart(fig1, use_container_width=True)

# Update teks analisis mengikut peratus
st.write(f"""
The graph above shows the percentage importance of factors that contribute to traffic congestion. 
Factor **{factor_means.iloc[-1]['Factor']}** recorded the highest percentage of **{factor_means.iloc[-1]['Percentage']:.1f}%**, 
followed by other infrastructure factors.
""")
st.markdown("---")
    # --- SECTION 2: DEMOGRAPHIC COMPARISON ---
    st.subheader("City Demographic Analysis")
    if 'Area Type' in data.columns:
        melted_data = data.melt(id_vars=['Area Type'], value_vars=factor_cols, var_name='Factor', value_name='Score')
        comparison_data = melted_data.groupby(['Area Type', 'Factor'])['Score'].mean().reset_index()
        fig2 = px.bar(comparison_data, x='Score', y='Factor', color='Area Type', barmode='group', orientation='h')
        st.plotly_chart(fig2, use_container_width=True)

    st.write("The graph illustrates the varying perceptions of congestion factors across Urban, Suburban, and Rural areas. Urban respondents highlighted parking shortages and aggressive driving as prominent issues, suggesting these lead to severe congestion. In Suburban areas, the focus was on the impact of construction and road works, attributed to infrastructure development aimed at accommodating population growth. Rural respondents pointed to narrow roads and road damage as significant concerns due to less maintained infrastructure. Additionally, the late drop-off and pick-up of children impacts congestion in all areas, particularly in urban settings. Overall, urban congestion is driven by parking issues, suburban areas by development disruptions, and rural regions by inadequate infrastructure quality.")

    st.markdown("---")

    # --- SECTION 3: HEATMAP ---
    st.subheader("🌡️ Heatmap Analysis")
    if 'Status' in data.columns:
        heatmap_df = data.groupby('Status')[factor_cols].mean()
        fig3 = px.imshow(heatmap_df, text_auto=".2f", aspect="auto")
        st.plotly_chart(fig3, use_container_width=True)

    st.write("The heatmap displays average scores on congestion factors regarding respondents' status, highlighting that university students and residents are most affected by traffic congestion near schools. This is reflected in high scores for these groups. Teachers show a moderate concern, particularly regarding entrance and exit factors. Key infrastructure issues, such as insufficient parking and narrow roads, score highly among students and parents, with residents particularly concerned about narrow roads. Consistent factors affecting all groups include rainy weather and road damage. User behavior factors are less significant, as respondents attribute more impact to infrastructure issues rather than road user behavior.")

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
    st.write("The diagram illustrates a bar chart detailing factors contributing to traffic congestion in front of schools and suggests solutions. Key issues include lack of parking, narrow roads, and behavioral factors like undisciplined driving. Recommendations to alleviate congestion focus on creating drop-off zones, deploying traffic officers, and enhancing road infrastructure. The graph reflects residents' calls for improved traffic control and physical infrastructure to address these concerns, emphasizing the need for better stopping spaces and road conditions to ensure smoother traffic in the future.")

except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
