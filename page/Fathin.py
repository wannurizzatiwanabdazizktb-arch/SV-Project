import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Analysis of Factors and Perceptions of Traffic Congestion in School Areas", layout="wide")

# 2. Masukkan URL data mentah
DATA_URL = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/main/project_dataSV_data.csv"

# 3. Baca data daripada GitHub (dengan Cache)
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    return df

data = load_data()

# --- PERSEDIAAN DATA ASAS ---
factor_cols = [col for col in data.columns if col.startswith('Faktor')]
kesan_cols = [col for col in data.columns if col.startswith('Kesan')]
langkah_cols = [col for col in data.columns if col.startswith('Langkah')]

# --- HEADER & CAPTION ---
st.title("📊 Analysis of Factors and Perceptions of Traffic Congestion in School Areas")
st.write(
    """
    This visual analysis reveals the main causes of congestion at schools through demographic and status comparisons. Through heatmaps and regression models, we can see how environmental factors influence traffic flow, helping to design more effective data-driven solutions.
    """
)

# --- 🟢 TEMPAT TERBAIK UNTUK KPI METRICS ---
# Kita gunakan filtered_data supaya nombor ini berubah bila filter dipilih
st.markdown("---")
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
with col_kpi1:
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

# --- BAHAGIAN 1: OVERALL AVERAGE SCORE ---
# Nota: Gunakan filtered_data di sini
factor_means = filtered_data[factor_cols].mean().sort_values(ascending=True)
plot_data_overall = factor_means.reset_index()
plot_data_overall.columns = ['Factor', 'Average Score']
plot_data_overall['Factor'] = plot_data_overall['Factor'].str.replace('Faktor ', '')

fig1 = px.bar(
    plot_data_overall, 
    x='Average Score', 
    y='Factor',
    orientation='h',
    title='<b>1. Average Factor Scores (Filtered)</b>',
    labels={'Average Score': 'Average Score', 'Factor': 'Factor'},
    color='Average Score',
    color_continuous_scale='Viridis',
    text_auto='.2f'
)
fig1.update_layout(xaxis_range=[0, 5], height=500)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# --- BAHAGIAN 2: DEMOGRAPHIC ANALYSIS ---
melted_data = filtered_data.melt(id_vars=['Jenis Kawasan'], value_vars=factor_cols, var_name='Factor', value_name='Average Score')
melted_data['Factor'] = melted_data['Factor'].str.replace('Faktor ', '')
comparison_data = melted_data.groupby(['Jenis Kawasan', 'Factor'])['Average Score'].mean().reset_index()

fig2 = px.bar(comparison_data, x='Average Score', y='Factor', color='Jenis Kawasan', barmode='group', orientation='h',
                 title='<b>2. Comparison: Area Types</b>', labels={'Jenis Kawasan': 'Area Type'}, text_auto='.2f')
fig2.update_layout(height=700)  
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# --- SECTION 3: HEATMAP ANALYSIS ---
st.subheader("🌡️ Heatmap Analysis")
if not filtered_data.empty:
    heatmap_df = filtered_data.groupby('Status')[factor_cols].mean()
    heatmap_df.columns = [col.replace('Faktor ', '') for col in heatmap_df.columns]
    fig3 = px.imshow(heatmap_df, color_continuous_scale='YlGnBu', title='<b>3. Heatmap: Factors by Status</b>', text_auto=".2f", aspect="auto")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")

st.markdown("---")

# --- BAHAGIAN 4: RELATIONSHIP ANALYSIS ---
st.subheader("🔗 Relationship Between Factors & Impacts")
col_scatter_1, col_scatter_2 = st.columns([1, 2])

with col_scatter_1:
    st.write("<b>Please select variables:</b>", unsafe_allow_html=True)
    f_select = st.selectbox("Select Factor (Paksi-X):", factor_cols)
    k_select = st.selectbox("Select Impact (Paksi-Y):", kesan_cols)

with col_scatter_2:
    if not filtered_data.empty:
        fig5 = px.scatter(
            filtered_data, 
            x=f_select, 
            y=k_select, 
            trendline="ols", 
            trendline_color_override="red", 
            opacity=0.5,
            title=f"Regression: {f_select.replace('Faktor ','')} vs {k_select.replace('Kesan ','')}"
        )
        st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# --- BAHAGIAN 5: CAUSE VS SOLUTION ---
st.subheader("💡 Summary: Main Causes vs. Proposed Solutions")
col5, col6 = st.columns(2)

f_means = filtered_data[factor_cols].mean().sort_values(ascending=True)
f_plot = f_means.reset_index()
f_plot.columns = ['Faktor', 'Skor']
f_plot['Faktor'] = f_plot['Faktor'].str.replace('Faktor ', '')

l_means = filtered_data[langkah_cols].mean().sort_values(ascending=True)
l_plot = l_means.reset_index()
l_plot.columns = ['Langkah', 'Skor']
l_plot['Langkah'] = l_plot['Langkah'].str.replace('Langkah ', '')

with col5:
    fig6 = px.bar(f_plot, x='Skor', y='Faktor', orientation='h',
                 title='<b>Main Causes (Factor)</b>',
                 color_discrete_sequence=['#e74c3c'], text_auto='.2f')
    fig6.update_layout(xaxis_range=[1, 5])
    st.plotly_chart(fig6, use_container_width=True)

with col6:
    fig7 = px.bar(l_plot, x='Skor', y='Langkah', orientation='h',
                 title='<b>Most Agreed Solutions (Measures)</b>',
                 color_discrete_sequence=['#2ecc71'], text_auto='.2f')
    fig7.update_layout(xaxis_range=[1, 5])
    st.plotly_chart(fig7, use_container_width=True)
