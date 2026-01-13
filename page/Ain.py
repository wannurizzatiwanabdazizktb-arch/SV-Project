import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# =========================================================
# 1. CONSTANTS & CONFIGURATION
# =========================================================
DATA_URL = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/cleaned_data.csv"

st.set_page_config(
    page_title="Traffic Congestion Survey Analysis",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# 2. DATA PROCESSING FUNCTIONS
# =========================================================
@st.cache_data
def load_data(url):
    """Fetch raw data from GitHub."""
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data from GitHub: {e}")
        return None

def process_disagreement_data(df):
    """Extract and aggregate Likert 1-2 responses."""
    # Define Likert Columns (Indices 3 to 27)
    likert_cols = df.columns[3:28].tolist()
    
    result_map = {}
    for col in likert_cols:
        # Filter rows where response is 1 (Strongly Disagree) or 2 (Disagree)
        result_map[col] = (
            df[df[col].isin([1, 2])]
            .groupby('Area Type')[col]
            .count()
        )
    
    disagreement_df = pd.DataFrame(result_map).fillna(0).astype(int)
    return disagreement_df, likert_cols

# =========================================================
# 3. UI STYLING (CSS)
# =========================================================
def apply_custom_styles():
    st.markdown("""
    <style>
        .center-title {
            text-align: center; font-size: 2.2rem; font-weight: 800;
            color: #1E293B; margin-bottom: 0.2rem;
        }
        .subtitle {
            text-align: center; font-size: 1.1rem; color: #64748b; margin-bottom: 1rem;
        }
        .divider {
            height: 2px; background: #e2e8f0; margin: 10px auto 30px auto; width: 90%;
        }
        div[data-testid="stMetric"] {
            background-color: #ffffff; border: 1px solid #e2e8f0;
            padding: 15px; border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# 4. MAIN APP EXECUTION
# =========================================================
def main():
    # Load and process
    df = load_data(DATA_URL)
    
    if df is not None:
        disagree_df, likert_cols = process_disagreement_data(df)
        
        # UI Header
        apply_custom_styles()
        st.markdown('<div class="center-title">Disagreement (Likert 1–2) Responses Across Area Type</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Nurul Ain Maisarah Binti Hamidin | S22A0064</div>', unsafe_allow_html=True) 
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
        # 5. DATA DISPLAY (Expander Section)
        # ---------------------------------------------------------
        # We use the pre-processed disagree_df from our earlier logic
        with st.expander("🔍 View Disagreement Count Table", expanded=False):
            st.write("#### Disagreement total each Likert Item Across Area Type")
            
            # Displaying as a professional, interactive dataframe
            st.dataframe(
                disagree_df, 
                use_container_width=True, 
                height=250 
            )
            
            st.caption("Note: This table shows responses for Likert 1 (Strongly Disagree) and 2 (Disagree) without outlier handling.")

        # ---------------------------------------------------------
        # 6. SUMMARY OVERVIEW (Metrics Section)
        # ---------------------------------------------------------
        # Custom Metric Styling
        st.markdown("""
        <style>
            [data-testid="stMetric"] {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            }
            [data-testid="stMetricValue"] {
                color: #0F172A !important;
                font-weight: 700;
            }
            [data-testid="stMetricLabel"] {
                color: #475569 !important;
                font-size: 0.9rem;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("### 📊 Summary Overview")

        # Layout using 4 columns for a dashboard feel
        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.metric(
                label="Total Disagreement", 
                value="191", 
                help="Breakdown: Effect (30) | Factor (130) | Step (31)",
                border=True
            )

        with m2:
            st.metric(
                label="Strongly Disagree (1)", 
                value="82", 
                help="Area: Rural (30) | Suburban (7) | Urban (45)", 
                border=True
            )

        with m3:
            st.metric(
                label="Disagree (2)", 
                value="109", 
                help="Area: Rural (31) | Suburban (13) | Urban (65)", 
                border=True
            )

        with m4:
            st.metric(
                label="Most Disagreement Item", 
                value="22", 
                help="Item: Late Drop-off/Pick-up Factor\nRural: 6\nSuburban: 4\nUrban: 12", 
                border=True
            )

        st.divider()
        
        # ---------------------------------------------------------
        # 7. VISUALIZATION SECTION (Ready for Charting)
        # ---------------------------------------------------------
        # You can now add your Plotly charts below here...

    else:
        st.error("Application stopped due to data loading error.")
        st.stop()

if __name__ == "__main__":
    main()
