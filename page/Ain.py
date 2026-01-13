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
        # Ensure the filename matches exactly
        df = pd.read_csv("cleaned_data.csv")
        
        # Define column ranges (Likert scale columns)
        likert_cols = df.columns[3:28].tolist()
        
        # Aggregate Disagreement (Likert 1 & 2) by Area Type
        result_map = {}
        for col in likert_cols:
            # Filter for 1 (Strongly Disagree) and 2 (Disagree)
            result_map[col] = (
                df[df[col].isin([1, 2])]
                .groupby('Area Type')[col]
                .count()
            )
        
        disagreement_df = pd.DataFrame(result_map).fillna(0).astype(int)
        return df, disagreement_df, likert_cols
    
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

# Load the data
merged_df, disagree_area_type_original, likert_cols = load_and_process_data()

if merged_df is None:
    st.error("CSV file not found or data format is incorrect. Please check 'cleaned_data.csv'.")
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

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="Traffic Survey Analysis", page_icon="📊", layout="wide")

# ---------------------------------------------------------
# 2. DATA LOADING (Updated to support Heatmap logic)
# ---------------------------------------------------------
@st.cache_data
def load_and_process_data():
    try:
        df = pd.read_csv("cleaned_data.csv")
        likert_cols = df.columns[3:28].tolist()
        
        # Categorize columns
        factor_cols = [col for col in likert_cols if 'Factor' in col]
        effect_cols = [col for col in likert_cols if 'Effect' in col]
        step_cols   = [col for col in likert_cols if 'Step' in col]
        
        # Prepare Heatmap Data
        heatmap_data = []
        for area in df['Area Type'].unique():
            for col in likert_cols:
                count_sd = df[(df['Area Type'] == area) & (df[col] == 1)].shape[0]
                count_d  = df[(df['Area Type'] == area) & (df[col] == 2)].shape[0]
                total = count_sd + count_d
                
                category = 'Factor' if col in factor_cols else 'Effect' if col in effect_cols else 'Step'
                if col == 'Students Not Sharing Vehicles': category = 'Special'
                
                heatmap_data.append({
                    'Area Type': area, 'Likert Item': col, 'Total': total,
                    'SD': count_sd, 'D': count_d, 'Category': category
                })
        
        return df, pd.DataFrame(heatmap_data), likert_cols, factor_cols, effect_cols, step_cols
    except Exception as e:
        st.error(f"Error: {e}")
        return None, None, None, None, None, None

merged_df, heatmap_df, likert_cols, factor_cols, effect_cols, step_cols = load_and_process_data()

# ---------------------------------------------------------
# 3. VISUALIZATION FUNCTIONS
# ---------------------------------------------------------

def draw_heatmap(df_heat):
    pivot_z = df_heat.pivot(index='Likert Item', columns='Area Type', values='Total').fillna(0)
    pivot_sd = df_heat.pivot(index='Likert Item', columns='Area Type', values='SD').fillna(0)
    pivot_d = df_heat.pivot(index='Likert Item', columns='Area Type', values='D').fillna(0)

    # Create customdata for SD and D counts
    customdata = np.stack([pivot_sd.values, pivot_d.values], axis=-1)

    fig = go.Figure(data=go.Heatmap(
        z=pivot_z.values, x=pivot_z.columns, y=pivot_z.index,
        colorscale='YlGnBu', text=pivot_z.values, texttemplate="%{text}",
        customdata=customdata,
        hovertemplate='<b>%{y}</b><br>Area: %{x}<br>Total: %{z}<br>SD (1): %{customdata[0]}<br>D (2): %{customdata[1]}<extra></extra>'
    ))
    fig.update_layout(height=800, title="Disagreement Heatmap (SD & D Breakdown)")
    return fig

def draw_bar_chart(df_heat):
    # Filter out the 'Special' category/item
    filtered = df_heat.groupby('Likert Item').agg({'Total': 'sum'}).reset_index()
    filtered = filtered[filtered['Likert Item'] != 'Students Not Sharing Vehicles']
    filtered = filtered.sort_values('Total', ascending=True)

    fig = px.bar(filtered, x='Total', y='Likert Item', orientation='h',
                 color='Total', color_continuous_scale='Viridis', height=700)
    fig.update_layout(template='plotly_white', title="Overall Disagreement (Excl. Outliers)")
    return fig

# ---------------------------------------------------------
# 4. STREAMLIT LAYOUT
# ---------------------------------------------------------
st.title("Traffic Congestion Survey: Analysis of Disagreement")

# SECTION 1: HEATMAP
with st.expander("🌡️ Disagreement Heatmap (Detailed Breakdown)", expanded=True):
    st.plotly_chart(draw_heatmap(heatmap_df), use_container_width=True)

# SECTION 2: BAR CHART
with st.expander("📊 Total Disagreement Rankings", expanded=False):
    st.plotly_chart(draw_bar_chart(heatmap_df), use_container_width=True)

# SECTION 3: SUMMARY TABLE
with st.expander("📋 Most & Least Disagreed Items (Summary Table)", expanded=False):
    # Logic to find extremes per category
    summary_rows = []
    # 1. Special case
    summary_rows.append(heatmap_df[heatmap_df['Likert Item'] == 'Students Not Sharing Vehicles'].groupby('Likert Item').sum(numeric_only=True).reset_index())
    
    # 2. Category extremes
    for cat in ['Factor', 'Effect', 'Step']:
        cat_data = heatmap_df[heatmap_df['Category'] == cat].groupby('Likert Item').sum(numeric_only=True).reset_index()
        if not cat_data.empty:
            cat_sorted = cat_data.sort_values('Total', ascending=False)
            summary_rows.append(cat_sorted.iloc[[0]])  # Most
            if len(cat_sorted) > 1:
                summary_rows.append(cat_sorted.iloc[[-1]]) # Least
    
    final_table = pd.concat(summary_rows).rename(columns={'Total': 'Total Count', 'SD': 'Total SD (1)', 'D': 'Total D (2)'})
    st.table(final_table[['Likert Item', 'Total Count', 'Total SD (1)', 'Total D (2)']])
