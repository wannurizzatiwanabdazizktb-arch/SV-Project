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
        
# =========================================================
# 7. HEATMAP: PATTERN REVELATION
# =========================================================
st.subheader("📍 Disagreement Patterns Across Area Types")
st.markdown("""
**Objective:** To analyze how respondents from different area types prioritize disagreements across 
factors, effects, and steps, revealing the specific patterns of each Likert scale item.
""")

# ... (Data preparation code for heatmap_pivot_z and customdata_array goes here) ...

fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_pivot_z.values,
    x=heatmap_pivot_z.columns,
    y=heatmap_pivot_z.index,
    colorscale='YlGnBu',
    text=heatmap_pivot_z.values,
    texttemplate="%{text}",
    hovertemplate='<b>%{y}</b><br>Area: %{x}<br>Total Disagreement: %{z}<br>Strongly Disagree (1): %{customdata[0]}<br>Disagree (2): %{customdata[1]}<extra></extra>',
    customdata=customdata_array
))

fig_heatmap.update_layout(
    height=800,
    template='plotly_white',
    margin=dict(l=200),
    xaxis_title="Area Type",
    yaxis_title="Likert Scale Item"
)

# Display Heatmap
st.plotly_chart(fig_heatmap, use_container_width=True)



# =========================================================
# 8. BAR CHART: COMPARATIVE IMPACT
# =========================================================
st.markdown("---")
st.subheader("📊 Comparative Total Disagreement")

# Filtered data (Excluding 'Students Not Sharing Vehicles')
filtered_df = disagreement_summary_df[
    disagreement_summary_df['Likert Item'] != 'Students Not Sharing Vehicles'
].copy()

fig_bar = px.bar(
    filtered_df.sort_values('Total Disagreement Count', ascending=True),
    x='Total Disagreement Count',
    y='Likert Item',
    orientation='h',
    color='Total Disagreement Count',
    color_continuous_scale='Viridis',
    hover_data=['Rural areas', 'Suburban areas', 'Urban areas'],
    height=700
)

fig_bar.update_layout(template='plotly_white', margin=dict(l=200))

# Display Bar Chart
st.plotly_chart(fig_bar, use_container_width=True)

# =========================================================
# 9. RESULT SUMMARY & INSIGHTS
# =========================================================
st.markdown("### 📝 Analysis Results")

# Key findings displayed in a clean box
st.info("""
**Key Findings:**
1. **Urban Dominance:** Urban areas consistently show higher disagreement counts across almost all items.
2. **Top Factor:** *Late Drop-off/Pick-up Factor* (22) is the most significant point of disagreement among the defined factors.
3. **Primary Step:** *Vehicle Sharing* (14) emerged as a major point of disagreement within the 'Step' category.
""")

# EXPANDER for the final table result
with st.expander("📊 View Detailed Most/Least Disagreement Table"):
    st.write("This table highlights the extremes (Most and Least) within each Likert category.")
    
    # Display the final summary table
    st.dataframe(
        final_filtered_result, 
        use_container_width=True,
        hide_index=True
    )
    
    st.caption("Categorized by Factor, Effect, and Step to highlight critical disagreement trends.")
