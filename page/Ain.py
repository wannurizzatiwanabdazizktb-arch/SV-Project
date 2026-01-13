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
# 3. CUSTOM STYLES (Refined for Aesthetics)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Main Title & Subtitle logic remains the same */
    .center-title {
        text-align: center; font-size: 2.5rem; font-weight: 850;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem; letter-spacing: -1.5px; line-height: 1.2;
    }
    
    .subtitle {
        text-align: center; font-size: 1.1rem; color: #444444; 
        font-weight: 500; font-family: 'Source Sans Pro', sans-serif; 
        letter-spacing: 0.5px; margin-bottom: 0.5rem;
    }

    /* --- NEW AESTHETIC DIVIDER --- */
    .aesthetic-divider {
        height: 5px;
        width: 40%; /* Shorter width looks more premium */
        margin: 20px auto 40px auto;
        border-radius: 50px;
        background: linear-gradient(90deg, 
            rgba(30,60,114,0) 0%, 
            rgba(30,60,114,1) 50%, 
            rgba(30,60,114,0) 100%);
        position: relative;
    }

    .aesthetic-divider::after {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 12px;
        height: 12px;
        background-color: #1e3c72;
        border: 3px solid #ffffff;
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(30,60,114,0.5);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. HEADER SECTION
# ---------------------------------------------------------
st.markdown('<div class="center-title">Disagreement (Likert 1–2) Responses across Area Types</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Nurul Ain Maisarah Binti Hamidin | S22A0064</div>', unsafe_allow_html=True)

# The New Divider Element
st.markdown('<div class="aesthetic-divider"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. DATA VISUALIZATION TABLE
# ---------------------------------------------------------

# Set expanded=False to ensure the expander is closed when the page loads
with st.expander("Data Disagreement Across Area Type Table", expanded=False):
    
    # Custom Styled Subheader using HTML and CSS
    st.markdown("""
        <style>
            .matrix-title {
                font-family: 'Inter', sans-serif;
                font-size: 1.5rem;
                font-weight: 700;
                color: #1e3c72; /* Matches your header theme */
                margin-top: 10px;
                margin-bottom: 15px;
            }
        </style>
        <div class="matrix-title">Disagreement Count Matrix</div>
    """, unsafe_allow_html=True)
    
    # Display the styled dataframe
    st.dataframe(disagree_area_type_original, use_container_width=True)

# Divider for clean separation
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. SUMMARY METRICS BOX
# ---------------------------------------------------------
st.markdown("""
    <style>
        .matrix-title {
            font-family: 'Inter', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e3c72;
            margin-top: 20px;
            margin-bottom: 15px;
        }
        /* Custom Styling for the Metric "Box" */
        [data-testid="stMetric"] {
            background-color: #ffffff;
            border: 2px solid #f0f2f6; /* Subtle border */
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); /* Soft shadow */
            transition: transform 0.2s ease-in-out;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-5px); /* Lift effect on hover */
            border-color: #1e3c72; /* Border turns blue on hover */
        }
    </style>
    <div class="matrix-title">Summary Statistics</div>
""", unsafe_allow_html=True)

# Create columns for metrics
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

with m_col1:
    st.metric(
        label="Total Disagreement",
        value="191",
        help="Rural Areas: 48 | Suburban Areas: 20 | Urban Areas: 123"
    )

with m_col2:
    st.metric(
        label="Strongly Disagree (1)",
        value="82",
        help="Rural Areas: 6 | Suburban Areas: 4 | Urban Areas: 72"
    )

with m_col3:
    st.metric(
        label="Disagree (2)",
        value="109",
        help="Rural Areas: 42 | Suburban Areas: 16 | Urban Areas: 51"
    )

with m_col4:
    st.metric(
        label="Most Disagreement Item",
        value="22",
        help="Late Drop-off/Pick-up Factor | Rural Areas: 6 | Suburban Areas: 4 | Urban Areas: 12"
    )

st.markdown("<br>", unsafe_allow_html=True) # Add some spacing
st.markdown("---")

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

# ---------------------------------------------------------
# 5. CATEGORY ANALYSIS (Stacked Chart & Category Table)
# ---------------------------------------------------------

with st.expander("📊 Category-Level Disagreement Analysis", expanded=True):
    
    # --- PART A: STACKED BAR CHART ---
    st.subheader("1. Disagreement by Category and Area Type")
    
    # We use heatmap_df created earlier to ensure consistency
    # (It already contains Category, Area Type, and Total Disagreement)
    fig_stacked = px.bar(
        heatmap_df, 
        x='Area Type', 
        y='Total', 
        color='Category',
        title='Stacked Disagreement Responses by Category (Detailed Hover)',
        labels={'Total': 'Number of Disagreements', 'Area Type': 'Area Type'},
        # Mapping colors to match your professional theme
        color_discrete_map={'Factor':'#1f77b4','Effect':'#ff7f0e','Step':'#2ca02c', 'Special': '#d62728'},
        hover_data={'Likert Item': True, 'Category': True, 'Total': True}
    )

    fig_stacked.update_layout(
        barmode='stack',
        template='plotly_white',
        height=500,
        xaxis={'categoryorder':'total descending'}
    )
    
    st.plotly_chart(fig_stacked, use_container_width=True)
    
    st.divider()

    # --- PART B: CATEGORY SUMMARY TABLE ---
    st.subheader("2. Total Disagreement Counts by Category")
    
    # Grouping the data for the category summary
    category_summary = heatmap_df.groupby('Category').agg({
        'Total': 'sum',
        'SD': 'sum',
        'D': 'sum'
    }).reset_index()

    # Calculate area-specific sums for the table
    area_pivot = heatmap_df.pivot_table(
        index='Category', 
        columns='Area Type', 
        values='Total', 
        aggfunc='sum'
    ).fillna(0).astype(int)

    # Merge overall totals with area totals
    final_cat_table = category_summary.merge(area_pivot, on='Category')
    
    # Rename columns for professional display
    final_cat_table = final_cat_table.rename(columns={
        'Total': 'Grand Total',
        'SD': 'Strongly Disagree (1)',
        'D': 'Disagree (2)'
    })

    st.write("Below is the consolidated disagreement count for each survey category across all regions:")
    st.dataframe(final_cat_table, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# 6. RURAL RESPONDENTS ANALYSIS (Bubble Chart & Table)
# ---------------------------------------------------------

with st.expander("🌾 Rural Area Deep-Dive (Bubble Chart & Summary)", expanded=False):
    
    # 1. Prepare Rural Data
    rural_df = merged_df[merged_df['Area Type'] == 'Rural areas']
    rural_disagreement_data = []

    for col in likert_cols:
        if col in rural_df.columns:
            count_sd = (rural_df[col] == 1).sum()
            count_d  = (rural_df[col] == 2).sum()
            
            # Identify category
            if 'Factor' in col: cat = 'Factor'
            elif 'Effect' in col: cat = 'Effect'
            elif 'Step' in col: cat = 'Step'
            else: cat = 'Other'

            if count_sd > 0:
                rural_disagreement_data.append({
                    'Likert Item': col, 'Category': cat,
                    'Count': count_sd, 'Level': 'Strongly Disagree (1)'
                })
            if count_d > 0:
                rural_disagreement_data.append({
                    'Likert Item': col, 'Category': cat,
                    'Count': count_d, 'Level': 'Disagree (2)'
                })

    df_bubble_rural = pd.DataFrame(rural_disagreement_data)

    if not df_bubble_rural.empty:
        # --- PART A: BUBBLE CHART ---
        st.subheader("1. Rural Disagreement Intensity (1 vs 2)")
        
        # Sort Y-axis for better readability
        df_bubble_rural = df_bubble_rural.sort_values(['Category', 'Count'])

        fig_bubble = px.scatter(
            df_bubble_rural,
            x='Count',
            y='Likert Item',
            size='Count',
            color='Level',
            color_discrete_map={'Strongly Disagree (1)':'#1f77b4','Disagree (2)':'#28a745'},
            hover_data=['Category', 'Count'],
            size_max=30,
            height=800,
            template='plotly_white'
        )
        
        fig_bubble.update_layout(
            xaxis_title='Number of Responses',
            yaxis_title='Likert Scale Item',
            legend_title_text='Disagreement Level'
        )
        
        st.plotly_chart(fig_bubble, use_container_width=True)

        st.divider()

        # --- PART B: RURAL SUMMARY TABLE ---
        st.subheader("2. Rural Disagreement Summary Table")
        
        # Create a pivoted table for the rural data
        rural_table = df_bubble_rural.pivot_table(
            index=['Category', 'Likert Item'], 
            columns='Level', 
            values='Count', 
            aggfunc='sum'
        ).fillna(0).reset_index()

        st.dataframe(rural_table, use_container_width=True, hide_index=True)
    else:
        st.write("No disagreement data found for Rural areas.")

# ---------------------------------------------------------
# FINAL FOOTER
# ---------------------------------------------------------
st.markdown("---")
st.caption("Streamlit Dashboard created for Traffic Congestion Survey Analysis © 2026")


import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. DEFINE FUNCTIONS AT THE TOP ---
def classify_item(col):
    """Categorizes survey items based on keywords."""
    if 'Factor' in col:
        return 'Factor'
    elif 'Effect' in col:
        return 'Effect'
    elif 'Step' in col:
        return 'Step'
    else:
        return 'Other'

# --- 2. URBAN EXPANDER ---
with st.expander("🏙️ Urban Area Detailed Breakdown", expanded=True):
    
    # Filter for Urban respondents
    urban_df = merged_df[merged_df['Area Type'] == 'Urban areas']
    
    disagreement_data = []
    # Ensure likert_cols is available from your previous data processing step
    for col in likert_cols:
        if col in urban_df.columns:
            count_sd = (urban_df[col] == 1).sum()
            count_d  = (urban_df[col] == 2).sum()

            if count_sd > 0 or count_d > 0:
                disagreement_data.append({
                    'Likert Scale Item': col,
                    'Item Category': classify_item(col),
                    'Strongly Disagree (1)': count_sd,
                    'Disagree (2)': count_d,
                    'Total': count_sd + count_d
                })

    if disagreement_data:
        disagreement_df = pd.DataFrame(disagreement_data).sort_values('Total')

        # --- PART A: PLOTLY FIGURE ---
        st.subheader("Urban Disagreement: Strongly Disagree vs Disagree")
        
        fig = go.Figure()

        # Strongly Disagree Trace
        fig.add_trace(go.Bar(
            x=disagreement_df['Strongly Disagree (1)'],
            y=disagreement_df['Likert Scale Item'],
            orientation='h',
            name='Strongly Disagree (1)',
            marker=dict(color='#1f77b4'),
            customdata=disagreement_df[['Item Category', 'Strongly Disagree (1)']],
            hovertemplate='<b>Item:</b> %{y}<br><b>Category:</b> %{customdata[0]}<br><b>Count:</b> %{customdata[1]}<extra></extra>'
        ))

        # Disagree Trace
        fig.add_trace(go.Bar(
            x=disagreement_df['Disagree (2)'],
            y=disagreement_df['Likert Scale Item'],
            orientation='h',
            name='Disagree (2)',
            marker=dict(color='#2ca02c'),
            customdata=disagreement_df[['Item Category', 'Disagree (2)']],
            hovertemplate='<b>Item:</b> %{y}<br><b>Category:</b> %{customdata[0]}<br><b>Count:</b> %{customdata[1]}<extra></extra>'
        ))

        fig.update_layout(
            barmode='group',
            xaxis_title='Number of Responses',
            yaxis_title='Likert Scale Item',
            legend_title_text='Disagreement Level',
            template='plotly_white',
            height=800,
            margin=dict(l=200)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # --- PART B: SUMMARY TABLE ---
        st.subheader("Summary Table: Urban Disagreement Counts")
        
        # Display as a clean Streamlit dataframe
        table_df = disagreement_df[['Likert Scale Item', 'Item Category', 'Strongly Disagree (1)', 'Disagree (2)']]
        st.dataframe(table_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No disagreement data found for Urban areas.")

# ---------------------------------------------------------
# 8. SUBURBAN RESPONDENTS ANALYSIS (Radar Chart & Table)
# ---------------------------------------------------------

with st.expander("🏘️ Suburban Area Deep-Dive (Radar Chart & Summary)", expanded=False):
    
    # Filter for Suburban respondents
    suburban_df = merged_df[merged_df['Area Type'] == 'Suburban areas']

    # Prepare disagreement data
    sub_dis_data = []
    for col in likert_cols:
        # Skip 'Students Not Sharing Vehicles' per your logic
        if col == 'Students Not Sharing Vehicles':
            continue
            
        if col in suburban_df.columns:
            count_sd = (suburban_df[col] == 1).sum()
            count_d  = (suburban_df[col] == 2).sum()
            
            if count_sd > 0 or count_d > 0:
                sub_dis_data.append({
                    'Likert Item': col,
                    'Category': classify_item(col),
                    'Strongly Disagree (1)': count_sd,
                    'Disagree (2)': count_d
                })

    df_suburban = pd.DataFrame(sub_dis_data)

    if not df_suburban.empty:
        # --- PART A: RADAR CHART ---
        st.subheader("1. Suburban Disagreement Radar Profile")
        st.write("_Excluding 'Students Not Sharing Vehicles'_")
        
        # Melt data for radar chart compatibility
        sub_melted = df_suburban.melt(
            id_vars=['Likert Item','Category'],
            value_vars=['Strongly Disagree (1)','Disagree (2)'],
            var_name='Disagreement Type',
            value_name='Count'
        )

        # Create radar chart
        fig_radar = px.line_polar(
            sub_melted,
            r='Count',
            theta='Likert Item',
            color='Disagreement Type',
            line_close=True,
            markers=True,
            color_discrete_map={'Strongly Disagree (1)':'#1f77b4','Disagree (2)':'#28a745'},
            template='plotly_white'
        )

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(title='Responses', visible=True, tickfont_size=10),
                angularaxis=dict(tickfont_size=9)
            ),
            height=800,
            margin=dict(t=50, b=50)
        )

        st.plotly_chart(fig_radar, use_container_width=True)

        st.divider()

        # --- PART B: SUMMARY TABLE ---
        st.subheader("2. Suburban Disagreement Summary Table")
        
        sub_summary = df_suburban[['Likert Item', 'Category', 'Strongly Disagree (1)', 'Disagree (2)']]
        st.dataframe(sub_summary, use_container_width=True, hide_index=True)
    else:
        st.info("No disagreement data found for Suburban areas (excluding outliers).")
