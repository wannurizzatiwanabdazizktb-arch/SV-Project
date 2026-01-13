# =========================================================
# Traffic Congestion Survey Analysis of Disagreement
# Structured Version — by Nurul Ain Maisarah Hamidin (2026)
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Traffic Congestion Survey Analysis",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------------
# 2. DATA LOADING & PROCESSING FUNCTIONS
# ---------------------------------------------------------
@st.cache_data
def load_and_process_data():
    try:
        df = pd.read_csv("cleaned_data.csv")
        
        # Define column ranges (Adjust indices as per your actual CSV)
        likert_cols = df.columns[3:28].tolist()
        
        # Identify categories based on keywords
        factor_cols = [col for col in likert_cols if 'Factor' in col]
        effect_cols = [col for col in likert_cols if 'Effect' in col]
        step_cols   = [col for col in likert_cols if 'Step' in col]
        
        # Aggregate Disagreement (Likert 1 & 2) by Area Type
        result_map = {}
        for col in likert_cols:
            result_map[col] = (
                df[df[col].isin([1, 2])]
                .groupby('Area Type')[col]
                .count()
            )
        
        disagreement_df = pd.DataFrame(result_map).fillna(0).astype(int)
        
        return df, disagreement_df, likert_cols
    
    except FileNotFoundError:
        return None, None, None

# Load the data
merged_df, disagree_area_type_original, likert_cols = load_and_process_data()

if merged_df is None:
    st.error("CSV file not found. Please ensure 'cleaned_data.csv' is in the folder.")
    st.stop()

# ---------------------------------------------------------
# 3. CUSTOM STYLES (CSS)
# ---------------------------------------------------------
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
    .metric-card {
        background: #ffffff; border-radius: 12px; padding: 15px;
        text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-bottom: 4px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. HEADER SECTION
# ---------------------------------------------------------
st.markdown('<div class="center-title">Disagreement (Likert 1–2) Responses across Area Types</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Nurul Ain Maisarah Binti Hamidin | S22A0064</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. DATA VISUALIZATION TABLE
# ---------------------------------------------------------
with st.expander("🔍 View Key Disagreement Insights", expanded=True):
st.subheader("Disagreement Count Matrix")
st.dataframe(disagree_area_type_original, use_container_width=True)

# ---------------------------------------------------------
# 6. KPI METRICS & INSIGHTS
# ---------------------------------------------------------
    st.write("### Analysis Summary")
    st.info("Analysis of how respondents across all area types selected 'Strongly Disagree' and 'Disagree'.")

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)

    with m_col1:
        st.metric(
            label="Most Disagreement: Factor",
            value="33",
            help="Students Not Sharing Vehicles: Rural (9), Suburban (6), Urban (18)."
        )

    with m_col2:
        st.metric(
            label="Most Disagreement: Effect",
            value="11",
            help="Unintended Road Accidents: Rural (1), Suburban (1), Urban (9)."
        )

    with m_col3:
        st.metric(
            label="Most Disagreement: Step",
            value="14",
            help="Vehicle Sharing Step: Rural (6), Suburban (2), Urban (6)."
        )

    with m_col4:
        st.metric(
            label="Lowest Disagreement",
            value="2",
            help="Pressure on Road User Effect: Rural (1), Suburban (0), Urban (1)."
        )

    st.markdown("---")
