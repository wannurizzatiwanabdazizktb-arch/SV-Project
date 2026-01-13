import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# 1. CONSTANTS & CONFIGURATION
# =========================================================
DATA_URL = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/cleaned_data.csv"

st.set_page_config(
    page_title="Traffic Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# 2. DATA PROCESSING
# =========================================================
@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def process_disagreement_data(df):
    likert_cols = df.columns[3:28].tolist()
    # Aggregating count of 1s and 2s
    res = df[df[likert_cols].isin([1, 2])].melt(id_vars=['Area Type'], value_vars=likert_cols)
    res = res.dropna().groupby(['Area Type', 'variable']).size().reset_index(name='Count')
    # Pivot for table view
    pivot_df = res.pivot(index='Area Type', columns='variable', values='Count').fillna(0).astype(int)
    return pivot_df, res

# =========================================================
# 3. MODERN UI STYLING (The "Beauty" Layer)
# =========================================================
def apply_custom_styles():
    st.markdown("""
    <style>
        /* Main background and font */
        .stApp {
            background-color: #FFFFFF;
            font-family: 'Inter', sans-serif;
        }
        
        /* Header Styling */
        .main-title {
            text-align: center; 
            font-size: 2.8rem; 
            font-weight: 800;
            background: linear-gradient(90deg, #1E293B, #4F46E5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0rem;
        }
        .author-sub {
            text-align: center; 
            font-size: 1rem; 
            color: #64748B; 
            letter-spacing: 1px;
            margin-bottom: 2rem;
        }
        
        /* Card-like containers for metrics */
        div[data-testid="stMetric"] {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease-in-out;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            border-color: #4F46E5;
        }
        
        /* Section Dividers */
        .section-header {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1E293B;
            border-left: 5px solid #4F46E5;
            padding-left: 15px;
            margin: 2rem 0 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# 4. MAIN APP
# =========================================================
def main():
    apply_custom_styles()
    df = load_data(DATA_URL)
    
    if df is not None:
        pivot_df, long_df = process_disagreement_data(df)

        # Header Section
        st.markdown('<h1 class="main-title">Traffic Congestion Analysis</h1>', unsafe_allow_html=True)
        st.markdown('<p class="author-sub">NURUL AIN MAISARAH BINTI HAMIDIN | S22A0064</p>', unsafe_allow_html=True)

        # --- Metrics Row ---
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Disagreement", "191", help="Combined Likert 1 & 2")
        m2.metric("Strongly Disagree (1)", "82")
        m3.metric("Disagree (2)", "109")
        m4.metric("Key Factor", "Late P/U")

        # --- Visualization Section ---
        st.markdown('<p class="section-header">Visual Insights</p>', unsafe_allow_html=True)
        
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            fig = px.bar(
                long_df, 
                x="Area Type", 
                y="Count", 
                color="Area Type",
                title="<b>Disagreement Volume by Area</b>",
                color_discrete_sequence=["#4F46E5", "#06B6D4", "#10B981"],
                template="plotly_white"
            )
            # FIXED: Removed invalid bordercolor
            fig.update_layout(
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            area_totals = long_df.groupby("Area Type")["Count"].sum().reset_index()
            fig_pie = px.pie(
                area_totals, 
                values='Count', 
                names='Area Type', 
                hole=0.5,
                title="<b>Distribution Ratio</b>",
                color_discrete_sequence=["#4F46E5", "#06B6D4", "#10B981"]
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)

        # --- Data Table Section ---
        st.markdown('<p class="section-header">Detailed Breakdown</p>', unsafe_allow_html=True)
        with st.expander("🔍 View Raw Disagreement Matrix", expanded=False):
            # Using a built-in pandas styler for a professional look
            st.dataframe(
                pivot_df.style.background_gradient(cmap="Blues"),
                use_container_width=True
            )
