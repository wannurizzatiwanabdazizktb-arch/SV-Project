import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. PAGE SETTINGS (Must be the first Streamlit command)
st.set_page_config(
    page_title="Traffic Congestion Survey Analysis",
    page_icon="📊",
    layout="wide"
)

# 2. LOAD DATA
@st.cache_data
def load_data():
    # Ensure this file exists in your directory
    return pd.read_csv("cleaned_data.csv")

try:
    merged_df = load_data()
except FileNotFoundError:
    st.error("CSV file not found. Please ensure 'cleaned_data.csv' is in the folder.")
    st.stop()

# 3. DEFINE COLUMNS & CATEGORIES
# Adjust indices [3:10] based on your actual CSV structure
likert_cols = merged_df.columns[3:28].tolist() 
factor_cols = [col for col in likert_cols if 'Factor' in col]
effect_cols = [col for col in likert_cols if 'Effect' in col]
step_cols   = [col for col in likert_cols if 'Step' in col]

# ---------------------------------------------------------
# MODULE 1: HEATMAP & OVERALL DISAGREEMENT
# ---------------------------------------------------------
st.title("📊 Traffic Congestion Disagreement Analysis")

heatmap_data = []
for area in merged_df["Area Type"].unique():
    for col in likert_cols:
        area_data = merged_df[merged_df["Area Type"] == area]
        sd = (area_data[col] == 1).sum()
        d = (area_data[col] == 2).sum()
        
        category = 'Factor' if col in factor_cols else 'Effect' if col in effect_cols else 'Step'

        heatmap_data.append({
            "Area Type": area,
            "Likert Item": col,
            "Category": category,
            "Total": sd + d,
            "SD": sd,
            "D": d
        })

heatmap_df = pd.DataFrame(heatmap_data)
pivot = heatmap_df.pivot(index="Likert Item", columns="Area Type", values="Total").fillna(0)

st.subheader("Global Disagreement Heatmap (Strongly Disagree + Disagree)")
fig_heatmap = go.Figure(go.Heatmap(
    z=pivot.values, x=pivot.columns, y=pivot.index,
    colorscale="YlGnBu", text=pivot.values, texttemplate="%{text}"
))
st.plotly_chart(fig_heatmap, use_container_width=True)

# ---------------------------------------------------------
# MODULE 2: STACKED CATEGORY ANALYSIS
# ---------------------------------------------------------
st.markdown("---")
st.subheader("Disagreement by Category and Area")

fig_stacked = px.bar(
    heatmap_df, x='Area Type', y='Total', color='Category',
    title='Stacked Disagreement Responses by Category',
    barmode='stack', template='plotly_white',
    color_discrete_map={'Factor':'#1f77b4','Effect':'#ff7f0e','Step':'#2ca02c'}
)
st.plotly_chart(fig_stacked, use_container_width=True)

# ---------------------------------------------------------
# MODULE 3: INDIVIDUAL AREA BREAKDOWN (TABS)
# ---------------------------------------------------------
st.markdown("---")
st.header("Deep Dive by Area Type")
tab1, tab2, tab3 = st.tabs(["Rural areas", "Urban areas", "Suburban areas"])

def create_area_analysis(area_name, color_sd, color_d):
    area_df = heatmap_df[heatmap_df['Area Type'] == area_name].sort_values('Total', ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(y=area_df['Likert Item'], x=area_df['SD'], name='SD (1)', orientation='h', marker_color=color_sd))
    fig.add_trace(go.Bar(y=area_df['Likert Item'], x=area_df['D'], name='D (2)', orientation='h', marker_color=color_d))
    fig.update_layout(barmode='group', height=700, title=f"Disagreement in {area_name}")
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(area_df[['Likert Item', 'Category', 'SD', 'D', 'Total']].sort_values('Total', ascending=False), hide_index=True)

with tab1:
    create_area_analysis("Rural areas", "#1f77b4", "#28a745")

with tab2:
    create_area_analysis("Urban areas", "#1f77b4", "#2ca02c")

with tab3:
    # Radar Chart for Suburban as requested in your snippets
    sub_df = heatmap_df[heatmap_df['Area Type'] == 'Suburban areas']
    sub_melted = sub_df.melt(id_vars=['Likert Item'], value_vars=['SD', 'D'], var_name='Type', value_name='Count')
    
    fig_radar = px.line_polar(sub_melted, r='Count', theta='Likert Item', color='Type', line_close=True, markers=True)
    st.plotly_chart(fig_radar, use_container_width=True)
    st.dataframe(sub_df[['Likert Item', 'SD', 'D', 'Total']], hide_index=True)
