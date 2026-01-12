# =========================================================
# Traffic Congestion Survey Analysis of Disagreement Likert Item
# Enhanced Version — by Nurul Ain Maisarah Hamidin (2026)
# =========================================================
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

# 4. DEFINE COLUMNS & CATEGORIES
# Assuming merged_df and likert_cols are already defined

result_original = {}

for col in likert_cols:
    result_original[col] = (
        merged_df[merged_df[col].isin([1, 2])]
        .groupby('Area Type')[col]
        .count()
    )

# Create the DataFrame and fill missing values
disagree_area_type_original = pd.DataFrame(result_original).fillna(0).astype(int)

# --- Streamlit Display Section ---

st.markdown("""
<style>
    .center-title {
        text-align: center; font-size: 2.2rem; font-weight: 800;
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem; letter-spacing: -1px;
    }
    .subtitle {
        text-align: center; font-size: 1rem; color: #666;
        font-family: 'Inter', sans-serif; letter-spacing: 1px; margin-bottom: 1rem;
    }
    .divider {
        height: 3px; background: linear-gradient(90deg, transparent, #4facfe, #764ba2, transparent);
        margin: 10px auto 30px auto; width: 80%; border-radius: 50%;
    }
    /* Unified Expander Style */
    .stExpander {
        background-color: #1E1E1E !important;
        border: 2px solid #4facfe !important;
        border-radius: 15px !important;
        animation: glow 3s infinite;
    }
    @keyframes glow {
        0% { box-shadow: 0 0 5px #4facfe; }
        50% { box-shadow: 0 0 20px #00f2fe; }
        100% { box-shadow: 0 0 5px #4facfe; }
    }
    .metric-card {
        background: #ffffff; border-radius: 12px; padding: 15px;
        text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-bottom: 4px solid #ddd; transition: 0.2s;
    }
    .metric-card:hover { transform: translateY(-3px); }
</style>
""", unsafe_allow_html=True)

# --------------------
# 3. Header Section
# --------------------
st.markdown('<div class="center-title">isagreement (Likert 1–2) responses across Area Types</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Nurul Ain Maisarah Binti Hamidin | S22A0064</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Option 1: Interactive Table (Allows sorting and resizing)
st.dataframe(disagree_area_type_original, use_container_width=True)

# Option 2: Static Table (Better for simple, non-interactive reports)
# st.table(disagree_area_type_original)

# ---------------------------------------------------------
# KPI METRICS (INTERPRETIVE SUMMARY BOX)
# ---------------------------------------------------------
with st.expander(
    "Most Disagreement Count on Factor, Effect & Step",
    expanded=False
    

    st.subheader(
        "How respondents from all area types choose most disagreements (factors, effects, and step), "
        "to reveal the pattern of each Likert scale item count."
    )

    st.markdown("## Most highly Disagreement Insights by Category")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="Most Disagreement Factor",
        value="33",
        help=(
            "Students Not Sharing Vehicles. "
            "Rural areas (9), "
            "Suburban areas (6), "
            "Urban areas (18). "
            "Disagree (20) and Strongly Disagree (13). "
        )
    )

    col2.metric(
        label="Most Disagreement Effect",
        value="11",
        help=(
            "Unintended Road Accidents Effect. "
            "Rural areas (1), "
            "Suburban areas (1), "
            "Urban areas (9). "
            "Disagree (9) and Strongly Disagree (2). "
        )
    )

    col3.metric(
        label="Most Disagreement Step",
        value="14",
        help=(
            "Vehicle Sharing Step, "
            "Rural areas (6), "
            "Suburban areas (2), "
            "Urban areas (6). "
            "Disagree (8) and Strongly Disagree (6). "
        )
    )

    col4.metric(
        label="Lowest Disagreement Item",
        value="2",
        help=(
            "Pressure on Road User Effect, "
            "Rural areas (1), "
            "Suburban areas (0), "
            "Urban areas (1). "
            "Disagree (1) and Strongly Disagree (1). "
        )
    )

    st.markdown("---")

