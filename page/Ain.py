# =========================================================
# Traffic Congestion Survey Analysis of Disagreement
# Cloud Version (GitHub) — by Nurul Ain Maisarah Hamidin
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
# 2. DATA LOADING & PROCESSING (GITHUB SOURCE)
# ---------------------------------------------------------
@st.cache_data
def load_and_process_data():
    # YOUR RAW GITHUB URL
    URL = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/cleaned_data.csv"
    
    try:
        # Pandas can read directly from the URL
        df = pd.read_csv(URL)
        
        # Define Likert Columns (assuming they start from index 3 to 27)
        likert_cols = df.columns[3:28].tolist()
        
        # Aggregate Disagreement (Likert 1 & 2) by Area Type
        result_map = {}
        for col in likert_cols:
            # Filters rows where response is 1 or 2, then counts by Area Type
            result_map[col] = (
                df[df[col].isin([1, 2])]
                .groupby('Area Type')[col]
                .count()
            )
        
        disagreement_df = pd.DataFrame(result_map).fillna(0).astype(int)
        
        return df, disagreement_df, likert_cols
    
    except Exception as e:
        st.error(f"Error loading data from GitHub: {e}")
        return None, None, None

# Load the data
merged_df, disagree_area_type_original, likert_cols = load_and_process_data()

if merged_df is None:
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
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center; font-size: 1rem; color: #666; margin-bottom: 1rem;
    }
    .divider {
        height: 3px; background: linear-gradient(90deg, transparent, #4facfe, #764ba2, transparent);
        margin: 10px auto 30px auto; width: 80%;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. HEADER SECTION
# ---------------------------------------------------------
st.markdown('<div class="center-title">Disagreement (Likert 1–2) Responses</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Nurul Ain Maisarah Binti Hamidin | S22A0064</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA PROCESSING: Disagreement Counts by Area Type
# ---------------------------------------------------------
# This logic creates the DataFrame based on Likert values 1 and 2
result_original = {}

for col in likert_cols:
    result_original[col] = (
        merged_df[merged_df[col].isin([1, 2])]
        .groupby('Area Type')[col]
        .count()
    )

# Create the DataFrame, fill missing values with 0, and convert to integer
disagree_area_type_original = pd.DataFrame(result_original).fillna(0).astype(int)

# ---------------------------------------------------------
# 5. DATA DISPLAY: PROFESSIONAL DESIGN (Streamlit Version)
# ---------------------------------------------------------
with st.expander("Before Outlier Disagreement Table", expanded=True):
    st.markdown("### Disagreement across Area Type")

    # Apply professional styling to the DataFrame
    # 1. Background gradient (Heatmap) to identify high values quickly
    # 2. Highlight the maximum value in each column
    # 3. Format with thousand separators
    styled_df = disagree_area_type_original.style \
        .background_gradient(cmap='YlGnBu', axis=0) \
        .highlight_max(axis=0, color='#FFD700') \
        .format("{:,}")

    # Display using Streamlit's native dataframe component
    # This replaces display(HTML(...)) and provides a much better UI
    st.dataframe(
        styled_df, 
        use_container_width=True, 
        height=500
    )

    st.caption("💡 Darker blue cells indicate higher levels of disagreement. Yellow highlights show the highest item per area.*")
    
