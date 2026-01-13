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

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# ... (Previous imports and page config) ...

# 1. DEFINE CATEGORIES (Crucial to prevent NameErrors)
factor_cols = ['Rainy Weather Factor', 'Increasing Population Factor', 'Undisciplined Driver Factor', 
               'Damaged Road Factor', 'Leaving Work Late Factor', 'Single Gate Factor', 
               'Lack of Pedestrian Bridge Factor', 'Lack of Parking Space Factor', 
               'Late Drop-off/Pick-up Factor', 'Construction/Roadworks Factor', 'Narrow Road Factor']

effect_cols = ['Unintended Road Accidents Effect', 'Time Wastage Effect', 'Pressure on Road Users Effect', 
               'Students Late to School Effect', 'Environmental Pollution Effect', 'Fuel Wastage Effect']

step_cols = ['Widening Road Step', 'Vehicle Sharing Step', 'Two Gates Step', 'Arrive Early Step', 
             'Special Drop-off Area Step', 'Pedestrian Bridge Step', 'Traffic Officers Step']

all_likert_cols = factor_cols + effect_cols + step_cols + ['Students Not Sharing Vehicles']

# 2. DATA PREPARATION (Ensure this runs before the Chart)
heatmap_data_detailed = []

# Using merged_df (which should be loaded via your load_data function)
for area in ['Rural areas', 'Suburban areas', 'Urban areas']:
    for col in all_likert_cols:
        if col in merged_df.columns:
            count_sd = merged_df.loc[merged_df['Area Type'] == area, col].isin([1]).sum()
            count_d  = merged_df.loc[merged_df['Area Type'] == area, col].isin([2]).sum()
            total_disagreement_count = count_sd + count_d

            if total_disagreement_count > 0:
                heatmap_data_detailed.append({
                    'Area Type': area,
                    'Likert Item': col,
                    'Total Disagreement Count': total_disagreement_count,
                    'Strongly Disagree (1)': count_sd,
                    'Disagree (2)': count_d,
                    'Category': ('Factor' if col in factor_cols else 'Effect' if col in effect_cols else 'Step' if col in step_cols else 'Special')
                })

heatmap_df_detailed = pd.DataFrame(heatmap_data_detailed)

# 3. PIVOTING (This creates the 'heatmap_pivot_z' variable)
heatmap_pivot_z = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Total Disagreement Count').fillna(0)
heatmap_pivot_sd = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Strongly Disagree (1)').fillna(0)
heatmap_pivot_d = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Disagree (2)').fillna(0)

# Create customdata for hover effects
customdata_array = np.dstack((heatmap_pivot_sd.values, heatmap_pivot_d.values))

# 4. STREAMLIT DISPLAY
st.subheader("📍 Disagreement Patterns Across Area Types")
st.markdown("""
**Objective:** To analyze how respondents from all area types choose most disagreements (factors, effects, and step), 
to reveal the pattern of each Likert scale item count.
""")

# Create Figure
fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_pivot_z.values,
    x=heatmap_pivot_z.columns,
    y=heatmap_pivot_z.index,
    colorscale='YlGnBu',
    text=heatmap_pivot_z.values,
    texttemplate="%{text}",
    hovertemplate='<b>%{y}</b><br>Area: %{x}<br>Total Disagreement: %{z}<br>SD: %{customdata[0]}<br>D: %{customdata[1]}<extra></extra>',
    customdata=customdata_array
))

fig_heatmap.update_layout(height=800, template='plotly_white')
st.plotly_chart(fig_heatmap, use_container_width=True)



# 5. RESULT SUMMARY EXPANDER
with st.expander("📊 View Detailed Summary and Statistical Results"):
    # Place your final_filtered_result table logic here
    st.dataframe(final_filtered_result, use_container_width=True)
    st.write("The heatmap reveals that Urban areas show the highest concentration of disagreement, particularly regarding drop-off factors.")
    
        
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
