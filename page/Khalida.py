import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set(style="whitegrid")

@st.cache_data
def load_data():
    df = pd.read_csv("traffic_survey.csv")
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
    return df

df = load_data()

effect_cols = [
    "Unintended Road Accidents Effect",
    "Time Wastage Effect",
    "Pressure on Road Users Effect",
    "Students Late to School Effect",
    "Environmental Pollution Effect",
    "Fuel Wastage Effect",
]

cause_cols = [
    "Undisciplined Driver Factor",
    "Narrow Road Factor",
    "Single Gate Factor",
    "Lack of Parking Space Factor",
]

# ---------- PAGE HEADER ----------
st.header("Effects of School-area Congestion")

st.markdown("""
Use the filters below to explore how respondents rate different effects of congestion
around schools, and how perceptions differ by gender, status, and area type.
""")

# ---------- GLOBAL FILTERS ----------
with st.sidebar:
    st.subheader("Global filters (Goal 2)")
    gender_filter = st.selectbox(
        "Gender",
        ["All"] + sorted(df["Gender"].dropna().unique().tolist())
    )
    status_filter = st.selectbox(
        "Status",
        ["All"] + sorted(df["Status"].dropna().unique().tolist())
    )
    area_filter = st.selectbox(
        "Area Type",
        ["All"] + sorted(df["Area Type"].dropna().unique().tolist())
    )
    chosen_effect = st.selectbox(
        "Focus on effect",
        effect_cols
    )
    show_corr = st.checkbox("Show cause–effect heatmap", value=True)

sub = df.copy()
if gender_filter != "All":
    sub = sub[sub["Gender"] == gender_filter]
if status_filter != "All":
    sub = sub[sub["Status"] == status_filter]
if area_filter != "All":
    sub = sub[sub["Area Type"] == area_filter]

st.write(f"Number of responses after filters: **{len(sub)}**")

if len(sub) == 0:
    st.warning("No data for this filter combination. Please change the filters.")
    st.stop()

# ---------- 1) SUMMARY + BAR ----------
st.subheader("1. Summary of effect scores")

mean_effects = sub[effect_cols].mean()
std_effects = sub[effect_cols].std()

summary_df = pd.DataFrame({
    "Mean": mean_effects.round(2),
    "Std": std_effects.round(2)
}).sort_values("Mean", ascending=False)

col_table, col_bar = st.columns([1, 1.2])

with col_table:
    st.dataframe(summary_df, use_container_width=True)

with col_bar:
    fig, ax = plt.subplots(fig
