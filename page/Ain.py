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

---------------------------------------------------------
# 1. DATA PROCESSING (Must come BEFORE visualizations)
# ---------------------------------------------------------

# Define your columns if not already defined
likert_cols = [
    'Rainy Weather Factor', 'Increasing Population Factor', 'Undisciplined Driver Factor',
    'Damaged Road Factor', 'Leaving Work Late Factor', 'Single Gate Factor',
    'Lack of Pedestrian Bridge Factor', 'Lack of Parking Space Factor', 
    'Late Drop-off/Pick-up Factor', 'Construction/Roadworks Factor', 'Narrow Road Factor', 
    'Unintended Road Accidents Effect', 'Time Wastage Effect', 'Pressure on Road Users Effect', 
    'Students Late to School Effect', 'Environmental Pollution Effect', 'Fuel Wastage Effect', 
    'Students Not Sharing Vehicles', 'Widening Road Step', 'Vehicle Sharing Step', 
    'Two Gates Step', 'Arrive Early Step', 'Special Drop-off Area Step', 
    'Pedestrian Bridge Step', 'Traffic Officers Step'
]

# Create Categorization Lists
factor_cols = [c for c in likert_cols if 'Factor' in c or 'Sharing Vehicles' in c]
effect_cols = [c for c in likert_cols if 'Effect' in c]
step_cols = [c for c in likert_cols if 'Step' in c]

# CALCULATE HEATMAP DATA
heatmap_data_detailed = []
for area in ['Rural areas', 'Suburban areas', 'Urban areas']:
    for col in likert_cols:
        # Assuming merged_df exists in your environment
        count_sd = merged_df.loc[merged_df['Area Type'] == area, col].isin([1]).sum()
        count_d  = merged_df.loc[merged_df['Area Type'] == area, col].isin([2]).sum()
        total_count = count_sd + count_d
        
        if total_count > 0:
            heatmap_data_detailed.append({
                'Area Type': area,
                'Likert Item': col,
                'Total Disagreement Count': total_count,
                'Strongly Disagree (1)': count_sd,
                'Disagree (2)': count_d,
                'Category': ('Factor' if col in factor_cols else 'Effect' if col in effect_cols else 'Step')
            })

processed_data = pd.DataFrame(heatmap_data_detailed)

# CREATE PIVOTS (The variables that were missing)
heatmap_pivot_z = processed_data.pivot(index='Likert Item', columns='Area Type', values='Total Disagreement Count').fillna(0)
heatmap_pivot_sd = processed_data.pivot(index='Likert Item', columns='Area Type', values='Strongly Disagree (1)').fillna(0)
heatmap_pivot_d = processed_data.pivot(index='Likert Item', columns='Area Type', values='Disagree (2)').fillna(0)

# CUSTOMDATA ARRAY for interactivity
customdata_array = np.dstack((heatmap_pivot_sd.values, heatmap_pivot_d.values))

# ---------------------------------------------------------
# 2. UI LAYOUT
# ---------------------------------------------------------

st.markdown("### 🎯 Research Objective")
st.info("How respondents from all area types choose most disagreements (factors, effects, and step), to reveal the pattern of each Likert scale item count.")

with st.expander("📊 View Detailed Heatmap & Bar Chart Analysis", expanded=False):
    
    # Heatmap
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_pivot_z.values,
        x=heatmap_pivot_z.columns,
        y=heatmap_pivot_z.index,
        colorscale='Greys',
        text=heatmap_pivot_z.values,
        texttemplate="%{text}",
        customdata=customdata_array,
        hovertemplate='<b>%{y}</b><br>Area: %{x}<br>Total: %{z}<br>SD (1): %{customdata[0]}<br>D (2): %{customdata[1]}<extra></extra>'
    ))
    fig_heatmap.update_layout(template='plotly_white', height=700)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Horizontal Bar Chart
    # (Using your disagreement_summary_df or processed_data)
    fig_bar = px.bar(
        processed_data.groupby('Likert Item')['Total Disagreement Count'].sum().reset_index().sort_values('Total Disagreement Count'),
        x='Total Disagreement Count', y='Likert Item', orientation='h',
        color='Total Disagreement Count', color_continuous_scale='Greys'
    )
    st.plotly_chart(fig_bar, use_container_width=True)


# --- 3. INTERPRETATION & ANALYSIS ---
st.markdown("### 🧐 Interpretation and Analysis")
with st.container(border=True):
    st.write("""
    Items with higher disagreement counts indicate that respondents perceive them as **less important** or **less viable**.
    
    * **Primary Factor:** The *"Late Drop-off/Pick-up Factor"* (22) showed significant disagreement, particularly in **Urban areas (12)**, where disagreement and strong disagreement were split evenly (11 each).
    * **Lowest Disagreement:** The *"Narrow Road Factor"* (5) had the least disagreement, suggesting a widespread recognition that road constraints are valid contributors to congestion.
    * **Behavioral vs. Infrastructure:** Analysis reveals that behavioral factors are viewed as less significant compared to infrastructure-related issues.
    * **Unintended Road Accidents (11):** Specifically in urban regions (9), the data suggests an unclear understanding of the direct cause-and-effect relationship between congestion and actual accidents.
    * **Vehicle Sharing Step (14):** Showing non-acceptance of proposals requiring personal behavior changes, with consistent disagreement across Rural (6) and Urban (6) settings.
    """)

# --- 4. SUMMARY OF EXTREMES (Highest & Lowest) ---
st.markdown("### 🏆 Extremes by Category")

# Function to get high/low for display
def get_extremes(df, category):
    cat_df = df[df['Category'] == category].sort_values('Count Disagreement', ascending=False)
    return cat_df.iloc[0], cat_df.iloc[-1]

# Extracting results (Assuming final_summary_df has Category column)
f_high, f_low = get_extremes(processed_data.groupby('Likert Item').agg({'Total Disagreement Count':'sum','Category':'first'}).reset_index().rename(columns={'Total Disagreement Count':'Count Disagreement'}), 'Factor')
e_high, e_low = get_extremes(processed_data.groupby('Likert Item').agg({'Total Disagreement Count':'sum','Category':'first'}).reset_index().rename(columns={'Total Disagreement Count':'Count Disagreement'}), 'Effect')
s_high, s_low = get_extremes(processed_data.groupby('Likert Item').agg({'Total Disagreement Count':'sum','Category':'first'}).reset_index().rename(columns={'Total Disagreement Count':'Count Disagreement'}), 'Step')

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Factors**")
    st.caption(f"Highest: {f_high['Likert Item']} ({int(f_high['Count Disagreement'])})")
    st.caption(f"Lowest: {f_low['Likert Item']} ({int(f_low['Count Disagreement'])})")

with col2:
    st.markdown("**Effects**")
    st.caption(f"Highest: {e_high['Likert Item']} ({int(e_high['Count Disagreement'])})")
    st.caption(f"Lowest: {e_low['Likert Item']} ({int(e_low['Count Disagreement'])})")

with col3:
    st.markdown("**Steps**")
    st.caption(f"Highest: {s_high['Likert Item']} ({int(s_high['Count Disagreement'])})")
    st.caption(f"Lowest: {s_low['Likert Item']} ({int(s_low['Count Disagreement'])})")

# --- 5. CONCLUSION ---
st.divider()
st.markdown("The most popular choices of disagreement per category are: **Students Not Sharing Vehicles** (Factor - 33), **Unintended Road Accidents Effect** (Effect - 11), and **Vehicle Sharing Step** (Step - 14).")
