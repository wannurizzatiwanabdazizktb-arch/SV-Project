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
# 3. CUSTOM STYLES 
# ---------------------------------------------------------
st.markdown("""
<style>
    .center-title {
        text-align: center; 
        font-size: 2.2rem; 
        font-weight: 800;
        color: #1E293B; /* Deep Slate Gray */
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center; 
        font-size: 1rem; 
        color: #64748b; 
        margin-bottom: 1rem;
    }
    .divider {
        height: 2px; 
        background: #e2e8f0; /* Soft gray line */
        margin: 10px auto 30px auto; 
        width: 90%;
    }
    /* Optional: Makes the metric cards look more professional on white */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. HEADER SECTION
# ---------------------------------------------------------
st.markdown('<div class="center-title">Disagreement (Likert 1–2) Responses Across Area Type</div>', unsafe_allow_html=True)
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

# --------------------
# 5. DATA DISPLAY 
# --------------------
# Setting expanded=False ensures the table is hidden until the user clicks it
with st.expander("Disagreement Count Across Area Type", expanded=False):
    
    result_original = {}

    for col in likert_cols:
        result_original[col] = (
            merged_df[merged_df[col].isin([1, 2])]
            .groupby('Area Type')[col]
            .count()
        )

    # Create the final DataFrame and ensure it uses integers for a cleaner look
    disagree_area_type_original = pd.DataFrame(result_original).fillna(0).astype(int)

    # Displaying as a professional, interactive dataframe without custom colors
    # use_container_width=True ensures it fits your screen perfectly
    st.dataframe(
        disagree_area_type_original, 
        use_container_width=True, 
        height=220 
    )
    
    st.caption("Disagreement total each Likert Item Across Area Type Without Handling Outlier.")

# --------------------
# 6. Summary Box
# --------------------

# --- 1. PROFESSIONAL MONOCHROME STYLES ---
st.markdown("""
<style>
    /* Professional Slate Metric Styling for native st.metric */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0; /* Soft gray border */
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    /* Set metric value to deep black for high contrast */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: 700;
    }
    /* Set metric label to professional dark gray */
    [data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SUMMARY OVERVIEW SECTION ---
st.markdown("### Summary Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Total Disagreement", 
    value="191", 
    help="Effect: 30 | Factor: 130 | Step: 31",
    border=True
)

col2.metric(
    label="Strongly Disagree (1)", 
    value="82", 
    help="Rural: 30 | Suburban: 7 | Urban: 45", 
    border=True
)

col3.metric(
    label="Disagree (2)", 
    value="109", 
    help="Rural: 31 | Suburban: 13 | Urban: 65", 
    border=True
)

col4.metric(
    label="Most Disagreement Item", 
    value="22", 
    help="Late Drop-off/Pick-up Factor\nRural: 6\nSuburban: 4\nUrban: 12", 
    border=True
)

st.divider() # Visual separator

# --------------------
# Stacked Bar Chart
# --------------------

def create_dashboard():
    st.title("Traffic Congestion Analysis Dashboard")

    # 1. Objective Section
    st.info("""
    **Objective:** How respondents from area type choose most disagreements (factors, effects, or step), 
    revealing gaps between real-world experiences and the survey’s assumptions.
    """)

    # 2. Expander for Disagreement Analysis (Closed by default)
    with st.expander("📊 View Disagreement Analysis by Category and Area", expanded=False):
        
        # --- Beautiful Plotly Chart ---
        # Using a more sophisticated color palette (Material Design style)
        color_map = {
            'Factor': '#636EFA', # Royal Blue
            'Step': '#EF553B',   # Sunset Orange
            'Effect': '#00CC96'  # Emerald Green
        }

        fig = px.bar(
            stacked_df,
            x='Area Type',
            y='Disagreement Count',
            color='Category',
            title='<b>Disagreement Counts (1 & 2) by Category and Area Type</b>',
            labels={'Disagreement Count': 'Responses', 'Area Type': 'Region'},
            color_discrete_map=color_map,
            hover_name='Likert Item',  # Highlights the specific question on hover
            hover_data={'Area Type': False, 'Disagreement Count': True},
            category_orders={"Area Type": ["Rural areas", "Suburban areas", "Urban areas"]}
        )

        fig.update_layout(
            barmode='stack',
            template='plotly_white',
            font=dict(family="Arial", size=12),
            hoverlabel=dict(bgcolor="white", font_size=13),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=80, b=40)
        )
        
        # Display Plotly Chart
        st.plotly_chart(fig, use_container_width=True)

        # --- Summary Table ---
        st.subheader("Total Disagreement Counts by Category")
        # Displaying the HTML table with Streamlit's native styling for better look
        st.dataframe(category_disagreement_summary, use_container_width=True, hide_index=True)

        # --- Results / Interpretation Section ---
        st.markdown("### 🔍 Analysis Result")
        st.success("""
        **Using stacked bar chart with title ‘Disagreement Counts (1 & 2) by Category and Area Type’:**
        
        * **Factor:** The highest number of disagreement counts is attained by "Factor" under all categories, 
        specifically in **urban areas (85)**, compared to rural (31) and suburban (14). This indicates that 
        respondents tend to disagree with the proposed factors causing traffic congestion, suggesting the 
        issue is far more complex or systemic for urbanites than the survey criteria suggest.
        
        * **Effects:** This category has the **lowest levels of disagreement** (Urban: 21, Suburban: 3, Rural: 6). 
        This shows that despite geographical variations, almost all respondents agree on the actual consequences 
        of traffic congestion.
        
        * **Steps:** Shows large inconsistency, diverging most in **urban areas (35)**, followed by rural (20) 
        and suburban (9). This questions the effectiveness or relevance of the proposed suggestions, which 
        may be deemed impractical or insufficient in dynamic urban traffic flows.
        
        **Conclusion:** "Factor" is the primary choice of disagreement, followed by "Step," then "Effect" categories.
        """)

# Run the function
if __name__ == "__main__":
    create_dashboard()
