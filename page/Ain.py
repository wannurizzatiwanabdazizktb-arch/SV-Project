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
# 2. DATA LOADING & PROCESSING
# ---------------------------------------------------------
@st.cache_data
def load_and_process_data():
    try:
        df = pd.read_csv("cleaned_data.csv")
        likert_cols = df.columns[3:28].tolist()
        
        factor_cols = [col for col in likert_cols if 'Factor' in col]
        effect_cols = [col for col in likert_cols if 'Effect' in col]
        step_cols   = [col for col in likert_cols if 'Step' in col]
        
        heatmap_list = []
        for area in df['Area Type'].unique():
            for col in likert_cols:
                count_sd = df[(df['Area Type'] == area) & (df[col] == 1)].shape[0]
                count_d  = df[(df['Area Type'] == area) & (df[col] == 2)].shape[0]
                total = count_sd + count_d
                
                cat = 'Factor' if col in factor_cols else 'Effect' if col in effect_cols else 'Step'
                if col == 'Students Not Sharing Vehicles': cat = 'Special'
                
                heatmap_list.append({
                    'Area Type': area, 'Likert Item': col, 'Total': total,
                    'SD': count_sd, 'D': count_d, 'Category': cat
                })
        
        return pd.DataFrame(heatmap_list)
    except Exception as e:
        st.error(f"Error processing data: {e}")
        return None

heatmap_df = load_and_process_data()

# ---------------------------------------------------------
# 3. HEADER
# ---------------------------------------------------------
st.title("Traffic Congestion Survey: Analysis of Disagreement")
st.markdown("### Nurul Ain Maisarah Binti Hamidin | S22A0064")

# ---------------------------------------------------------
# 4. SINGLE COMBINED EXPANDER
# ---------------------------------------------------------
with st.expander("🔍 Detailed Disagreement Analysis (Heatmap, Bar Chart & Table)", expanded=True):
    
    # --- PART A: HEATMAP ---
    st.subheader("1. Disagreement Distribution Heatmap")
    
    pivot_z = heatmap_df.pivot(index='Likert Item', columns='Area Type', values='Total').fillna(0)
    pivot_sd = heatmap_df.pivot(index='Likert Item', columns='Area Type', values='SD').fillna(0)
    pivot_d = heatmap_df.pivot(index='Likert Item', columns='Area Type', values='D').fillna(0)
    
    customdata = np.stack([pivot_sd.values, pivot_d.values], axis=-1)

    fig_heat = go.Figure(data=go.Heatmap(
        z=pivot_z.values, x=pivot_z.columns, y=pivot_z.index,
        colorscale='YlGnBu', text=pivot_z.values, texttemplate="%{text}",
        customdata=customdata,
        hovertemplate='<b>%{y}</b><br>Area: %{x}<br>Total: %{z}<br>SD (1): %{customdata[0]}<br>D (2): %{customdata[1]}<extra></extra>'
    ))
    fig_heat.update_layout(height=700, margin=dict(t=30, b=30))
    st.plotly_chart(fig_heat, use_container_width=True)

    st.divider()

    # --- PART B: HORIZONTAL BAR CHART & TABLE (Side by Side) ---
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.subheader("2. Overall Rankings")
        # Filter for the bar chart
        bar_data = heatmap_df.groupby('Likert Item').agg({'Total': 'sum'}).reset_index()
        bar_data = bar_data[bar_data['Likert Item'] != 'Students Not Sharing Vehicles']
        bar_data = bar_data.sort_values('Total', ascending=True)

        fig_bar = px.bar(bar_data, x='Total', y='Likert Item', orientation='h',
                         color='Total', color_continuous_scale='Viridis', height=600)
        fig_bar.update_layout(showlegend=False, margin=dict(l=200))
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("3. Key Insights Table")
        # Generate summary logic
        summary_rows = []
        # Add Special Item
        summary_rows.append(heatmap_df[heatmap_df['Category'] == 'Special'].groupby('Likert Item').sum(numeric_only=True).reset_index())
        
        # Add Top/Bottom per Category
        for cat in ['Factor', 'Effect', 'Step']:
            cat_data = heatmap_df[heatmap_df['Category'] == cat].groupby('Likert Item').sum(numeric_only=True).reset_index()
            if not cat_data.empty:
                cat_sorted = cat_data.sort_values('Total', ascending=False)
                summary_rows.append(cat_sorted.iloc[[0]])  # Most Disagreed
                if len(cat_sorted) > 1:
                    summary_rows.append(cat_sorted.iloc[[-1]]) # Least Disagreed
        
        final_table = pd.concat(summary_rows).rename(columns={
            'Total': 'Count', 'SD': 'Total SD', 'D': 'Total D'
        })
        
        st.write("Summary of Most and Least Disagreed Items:")
        st.dataframe(final_table[['Likert Item', 'Count', 'Total SD', 'Total D']], 
                     use_container_width=True, hide_index=True)

st.info("The heatmap shows area-specific counts, while the bar chart highlights overall trends excluding outliers.")
