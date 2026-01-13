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

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------------
# 1. DATA PROCESSING (Crucial: Define variables before UI)
# ---------------------------------------------------------

# Ensure merged_df exists (assuming it is loaded from gspread or local)
# merged_df = ... 

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

# Categorization Logic
factor_cols = [c for c in likert_cols if 'Factor' in c or 'Sharing Vehicles' in c]
effect_cols = [c for c in likert_cols if 'Effect' in c]
step_cols = [c for c in likert_cols if 'Step' in c]

# Pre-calculate Heatmap Data to avoid NameErrors in the UI section
heatmap_list = []
for area in ['Rural areas', 'Suburban areas', 'Urban areas']:
    for col in likert_cols:
        count_sd = merged_df.loc[merged_df['Area Type'] == area, col].isin([1]).sum()
        count_d  = merged_df.loc[merged_df['Area Type'] == area, col].isin([2]).sum()
        total_count = count_sd + count_d
        
        if total_count > 0:
            heatmap_list.append({
                'Area Type': area,
                'Likert Item': col,
                'Total Disagreement Count': total_count,
                'Strongly Disagree (1)': count_sd,
                'Disagree (2)': count_d,
                'Category': ('Factor' if col in factor_cols else 'Effect' if col in effect_cols else 'Step')
            })

processed_data = pd.DataFrame(heatmap_list)

# Generate Pivots for Plotly
heatmap_pivot_z = processed_data.pivot(index='Likert Item', columns='Area Type', values='Total Disagreement Count').fillna(0)
heatmap_pivot_sd = processed_data.pivot(index='Likert Item', columns='Area Type', values='Strongly Disagree (1)').fillna(0)
heatmap_pivot_d = processed_data.pivot(index='Likert Item', columns='Area Type', values='Disagree (2)').fillna(0)

# Interactivity array (SD and D counts for hover)
customdata_array = np.dstack((heatmap_pivot_sd.values, heatmap_pivot_d.values))

# ---------------------------------------------------------
# 2. UI LAYOUT & VISUALS
# ---------------------------------------------------------

st.markdown("### 🎯 Research Objective")
st.info("""**Objective:** How respondents from all area types choose most disagreements (factors, effects, and step), 
to reveal the pattern of each Likert scale item count and perceive viability in traffic issues.""")

# Visualization Expander (Closed by default)
with st.expander("📊 View Detailed Heatmap & Bar Chart Analysis", expanded=False):
    
    # Monochrome Heatmap
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
    fig_heatmap.update_layout(title="Disagreement Responses Across Area Types", template='plotly_white', height=700)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Monochrome Bar Chart
    bar_data = processed_data.groupby('Likert Item')['Total Disagreement Count'].sum().reset_index().sort_values('Total Disagreement Count')
    fig_bar = px.bar(
        bar_data, x='Total Disagreement Count', y='Likert Item', orientation='h',
        title='Total Disagreement Counts Across All Areas',
        color='Total Disagreement Count', color_continuous_scale='Greys'
    )
    fig_bar.update_layout(template='plotly_white', height=700)
    st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------------------------------------
# 3. ANALYSIS & SUMMARY
# ---------------------------------------------------------

st.markdown("### 🧐 Interpretation and Analysis")
with st.container(border=True):
    st.write("""
    The **Late Drop-off/Pick-up Factor** (22) showed the highest overall disagreement, specifically in **Urban areas** (12). 
    In contrast, the **Narrow Road Factor** (5) recorded the lowest disagreement, indicating its high recognition as a true traffic contributor. 
    Analysis shows behavioral factors are often viewed as less viable than physical infrastructure steps.
    """)

st.markdown("### 🏆 Extremes by Category")

# Helper function for extremes
def get_extremes(df, category):
    cat_df = df[df['Category'] == category].sort_values('Count Disagreement', ascending=False)
    return cat_df.iloc[0], cat_df.iloc[-1]

# Summary Data Preparation
summary_agg = processed_data.groupby(['Likert Item', 'Category'])['Total Disagreement Count'].sum().reset_index()
summary_agg.columns = ['Likert Item', 'Category', 'Count Disagreement']

f_h, f_l = get_extremes(summary_agg, 'Factor')
e_h, e_l = get_extremes(summary_agg, 'Effect')
s_h, s_l = get_extremes(summary_agg, 'Step')

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**Factors**")
    st.caption(f"🔼 Highest: {f_h['Likert Item']} ({int(f_h['Count Disagreement'])})")
    st.caption(f"🔽 Lowest: {f_l['Likert Item']} ({int(f_l['Count Disagreement'])})")
with c2:
    st.markdown("**Effects**")
    st.caption(f"🔼 Highest: {e_h['Likert Item']} ({int(e_h['Count Disagreement'])})")
    st.caption(f"🔽 Lowest: {e_l['Likert Item']} ({int(e_l['Count Disagreement'])})")
with c3:
    st.markdown("**Steps**")
    st.caption(f"🔼 Highest: {s_h['Likert Item']} ({int(s_h['Count Disagreement'])})")
    st.caption(f"🔽 Lowest: {s_l['Likert Item']} ({int(s_l['Count Disagreement'])})")

st.divider()
st.markdown("**Conclusion:** The most popular choices of disagreement per category are: **Students Not Sharing Vehicles** (Factor - 33), **Unintended Road Accidents Effect** (Effect - 11), and **Vehicle Sharing Step** (Step - 14).")
