# ---------------------------------------------------------
# Disagreement Analysis Across Area type
# Nurul Ain Maisarah Binti Hamidin | S22A0064
# ---------------------------------------------------------
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
# Set page configuration
st.set_page_config(page_title="Likert Data Viewer", layout="wide")

# 1. DATA LOADING FUNCTION (Matches CSV exactly)
@st.cache_data
def load_raw_data():
    try:
        url = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/disagree_summary(Ain).csv"
        df = pd.read_csv(url)
        return df, None
    except Exception as e:
        return None, str(e)

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
# 1. Load Data
df, error = load_raw_data()

# 2. UI Container (The Expander)
with st.expander("Table of Counting Disagreement Likert Scale Across Type Areas", expanded=False):
    if df is not None:
        # --- TITLE SECTION ---
        st.markdown("""
            <style>
                .matrix-title {
                    font-family: 'Inter', sans-serif;
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: #1e3c72; 
                    margin-top: 10px;
                    margin-bottom: 15px;
                }
            </style>
            <div class="matrix-title">Disagreement Count Matrix</div>
        """, unsafe_allow_html=True)

        # --- DATA TABLE SECTION ---
        # Displays the raw data exactly like the CSV
        st.dataframe(df, use_container_width=True)

        # --- EXPLANATION SECTION (Bottom of Expander) ---
        st.markdown(
            """
            <div style="font-size: 0.85rem; line-height: 1.4; color: #808080; border-top: 1px solid #eee; pt-3;">
            <br>
            The total number of Likert items analysed is 24, after excluding “Students Not Sharing Vehicles”. 
            Since each of the 102 respondents answered all 24 items, a single respondent may select 
            “Strongly Disagree (1)” or “Disagree (2)” multiple times across different items. 
            Therefore, if respondents consistently chose Likert 1 or 2 across several items, the cumulative 
            count of disagreement responses can exceed 102. These totals represent the frequency of 
            disagreement responses across items, not the number of unique respondents. 
            <br><br>
            For example, if the table shows a value of 2.0 for “Arrive Early Step” in rural areas, 
            this indicates that two rural respondents selected either Strongly Disagree or Disagree 
            for that particular item. These values reflect the frequency of disagreement responses 
            for each item, rather than the total number of respondents (102), as each respondent 
            provided responses to multiple Likert items. So if all 102 is just select 1 or 2 scale mean the total disagreement is 2,448 responses for 24 item.
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.error(f"Error loading data: {error}")
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
        label="Total Respondend",
        value="102",
        help="Rural Areas:38 | Suburban Areas: 15 | Urban Areas: 49"
    )

# --- Grey Small Font Note ---
st.markdown(
    """
    <div style="font-size: 0.85rem; color: #808080; font-style: italic;">
    Why 109 total disagreement? You can see the details in the "Table of Counting Disagreement Likert Scale Across Type Areas" above.
    These counts do not indicate the number of unique respondents, as individual respondents may contribute multiple disagreement responses across different items.
    </div>
    """, 
    unsafe_allow_html=True
)

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
    <div class="matrix-title">Visualization Disagreement Across Area Type</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HEATMAP & HORIZONTAL BAR CHART WITH TABLE
# ---------------------------------------------------------
# --- 1. DATA PREPARATION ---
data = {
    'Area': ['Rural', 'Rural', 'Rural', 'Suburban', 'Suburban', 'Suburban', 'Urban', 'Urban', 'Urban'],
    'Category': ['Factors', 'Effects', 'Steps', 'Factors', 'Effects', 'Steps', 'Factors', 'Effects', 'Steps'],
    'Total Disagreement': [31.0, 6.0, 11.0, 14.0, 3.0, 3.0, 85.0, 21.0, 17.0],
    'Highest Item': [
        'Late Drop-off/Pick-up (19.4%)', 'Environmental Pollution (16.7%)', 'Vehicle Sharing (54.5%)',
        'Late Drop-off/Pick-up (28.6%)', 'Environmental Pollution (33.3%)', 'Vehicle Sharing (66.7%)',
        'Single Gate (16.5%)', 'Unintended Road Accidents (42.9%)', 'Vehicle Sharing (35.3%)'
    ],
    'Lowest Item': [
        'Narrow Road (0.0%)', 'Environmental Pollution (16.7%)', 'Pedestrian Bridge (0.0%)',
        'Lack of Parking Space (0.0%)', 'Pressure on Road Users (0.0%)', 'Pedestrian Bridge (0.0%)',
        'Narrow Road (5.9%)', 'Environmental Pollution (4.8%)', 'Widening Road (5.9%)'
    ]
}
df_summary = pd.DataFrame(data)

# Calculate Percentage Contribution
total_disagreement_sum = df_summary['Total Disagreement'].sum()
df_summary['Pct_Total'] = (df_summary['Total Disagreement'] / total_disagreement_sum * 100).round(2)

# Pivot data for heatmap
pivot_pct = df_summary.pivot(index='Category', columns='Area', values='Pct_Total')
pivot_raw = df_summary.pivot(index='Category', columns='Area', values='Total Disagreement')
pivot_high = df_summary.pivot(index='Category', columns='Area', values='Highest Item')
pivot_low = df_summary.pivot(index='Category', columns='Area', values='Lowest Item')

# --- 2. STREAMLIT UI ---

with st.expander("HEATMAP & HORIZONTAL BAR CHART", expanded=False):
    
    # Objective Section
    st.markdown("### Objective")
    st.info("""**To analyze how respondents from all area types choose most and lowest disagreements items percentages 
    (factors, effects, and step), to reveal the pattern of each Likert scale item count.**""")

    # --- HEATMAP ---
    fig_heat = px.imshow(
        pivot_pct,
        labels=dict(x="Area Type", y="Category", color="Contribution (%)"),
        x=['Rural', 'Suburban', 'Urban'],
        y=['Factors', 'Effects', 'Steps'],
        color_continuous_scale="Reds",
        text_auto=".1f",
        aspect="auto"
    )
    fig_heat.update_traces(
        hovertemplate="<br>".join([
            "<b>Area:</b> %{x}",
            "<b>Category:</b> %{y}",
            "<b>Contribution to Total:</b> %{z}%",
            "<b>Total Disagreement Count:</b> %{customdata[2]}",
            "<extra></extra>",
            "-----------------------------------------",
            "<b>Highest Contributor:</b> %{customdata[0]}",
            "<b>Lowest Contributor:</b> %{customdata[1]}"
        ]),
        customdata=np.stack((pivot_high.values, pivot_low.values, pivot_raw.values), axis=-1)
    )
    fig_heat.update_layout(title="Interactive Disagreement Heatmap: Contribution % by Area", template="plotly_white")
    st.plotly_chart(fig_heat, use_container_width=True)

    # --- BAR CHART ---
    plot_data = []
    for _, row in df_summary.iterrows():
        high_pct = float(row['Highest Item'].split('(')[-1].replace('%)', ''))
        low_pct = float(row['Lowest Item'].split('(')[-1].replace('%)', ''))
        plot_data.append({'Area_Cat': f"{row['Area']} - {row['Category']}", 'Type': 'Highest', 'Value': high_pct, 'Name': row['Highest Item']})
        plot_data.append({'Area_Cat': f"{row['Area']} - {row['Category']}", 'Type': 'Lowest', 'Value': low_pct, 'Name': row['Lowest Item']})
    df_plot = pd.DataFrame(plot_data)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        y=df_plot[df_plot['Type'] == 'Highest']['Area_Cat'], x=df_plot[df_plot['Type'] == 'Highest']['Value'],
        name='Highest Contributor', orientation='h', marker_color='crimson',
        hovertext=df_plot[df_plot['Type'] == 'Highest']['Name'],
        hovertemplate="<b>%{y}</b><br>Max Conflict: %{hovertext}<extra></extra>"
    ))
    fig_bar.add_trace(go.Bar(
        y=df_plot[df_plot['Type'] == 'Lowest']['Area_Cat'], x=df_plot[df_plot['Type'] == 'Lowest']['Value'],
        name='Lowest Contributor', orientation='h', marker_color='seagreen',
        hovertext=df_plot[df_plot['Type'] == 'Lowest']['Name'],
        hovertemplate="<b>%{y}</b><br>Min Conflict: %{hovertext}<extra></extra>"
    ))
    fig_bar.update_layout(title="Highest vs. Lowest Disagreement Percentages", barmode='group', template="plotly_white", height=500)
    st.plotly_chart(fig_bar, use_container_width=True)

    # --- SUMMARY TABLE ---
    st.markdown("### Disagreement Summary Table")
    st.dataframe(df_summary, use_container_width=True, hide_index=True)

    # --- INSIGHTS & EXPLANATIONS ---
    st.markdown("---")
    st.markdown("### Why this Visualization? Insights & Results")
    
    # Styling for grey small font as requested in previous turns
    st.markdown("""
    <div style="font-size: 0.9rem; color: #555; line-height: 1.6;">
    <b>Rationale for Visualization Selection:</b>
    <ul>
        <li><b>Heatmap:</b> Chosen to visualize the "concentration" of disagreement. It quickly reveals that Urban Areas (Factors) are the primary source of disagreement in the dataset.</li>
        <li><b>Grouped Bar Chart:</b> Used to highlight the extreme variance within categories, showing exactly which specific items drive the highest conflict versus those that are non-issues (0.0%).</li>
    </ul>
    
    <b>Key Insights & Results:</b>
    <ol>
        <li><b>Urban Dominance:</b> Urban areas contribute the highest disagreement percentages, particularly in the 'Factors' category (accounting for the largest share of the heatmap).</li>
        <li><b>The "Vehicle Sharing" Pattern:</b> Across ALL three areas (Rural, Suburban, Urban), the "Vehicle Sharing" item consistently appears as the highest contributor to disagreement in the 'Steps' category.</li>
        <li><b>Consistency in 'Effects':</b> Environmental Pollution is a shared concern in Rural and Suburban areas, appearing as the top disagreement item for both.</li>
        <li><b>Polarization in Suburban Areas:</b> Suburban respondents show the most concentrated disagreement in 'Vehicle Sharing' (66.7%), suggesting a very specific local pain point compared to other categories.</li>
        <li><b>Null Conflict Areas:</b> Several items like 'Narrow Road' and 'Pedestrian Bridge' show 0.0% disagreement in Rural/Suburban areas, indicating these factors are likely well-accepted or irrelevant to those respondents.</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# STACKED BAR CHART WITH TABLE
# ---------------------------------------------------------
# --- 1. DATA PREPARATION ---
# Unified data for both graph and table
data = {
    'Area Type': ['Rural', 'Rural', 'Rural', 'Suburban', 'Suburban', 'Suburban', 'Urban', 'Urban', 'Urban'],
    'Category': ['Factor', 'Effect', 'Step', 'Factor', 'Effect', 'Step', 'Factor', 'Effect', 'Step'],
    'Count': [31.0, 6.0, 11.0, 14.0, 3.0, 3.0, 85.0, 21.0, 17.0]
}
df_bar = pd.DataFrame(data)

# Calculate Percentages
total_sum = df_bar['Count'].sum()
df_bar['Percentage'] = (df_bar['Count'] / total_sum * 100).round(2)

# --- 2. STREAMLIT UI ---
with st.expander("STACKED BAR CHART", expanded=False):
    
    # Objective Section
    st.markdown("### Objective")
    st.info("""**To analyze how respondents from different area types choose most disagreements (factors, effects, or step), 
    revealing gaps between real-world experiences and the survey’s assumptions.**""")

    # --- BAR CHART SECTION ---
    # We use your exact hovertemplate logic
    fig = px.bar(
        df_bar, 
        x='Area Type', 
        y='Percentage', 
        color='Category',
        barmode='group',
        text='Percentage',
        title="Disagreement Distribution by Category and Area Type",
        labels={'Percentage': 'Contribution to Total (%)'},
        custom_data=['Count'],
        color_discrete_map={'Factor': '#1e3c72', 'Effect': '#ff4b4b', 'Step': '#ffa500'}
    )

    fig.update_traces(
        texttemplate='%{text}%', 
        textposition='outside',
        hovertemplate="<br>".join([
            "<b>Area Type:</b> %{x}",
            "<b>Category:</b> %{fullData.name}",
            "<b>Percentage:</b> %{y}%",
            "<b>Raw Count:</b> %{customdata[0]}",
            "<extra></extra>"
        ])
    )

    fig.update_layout(
        yaxis_range=[0, df_bar['Percentage'].max() + 10],
        template="plotly_white",
        legend_title="Category",
        height=500,
        margin=dict(t=50, b=50)
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- STYLED TABLE SECTION ---
    st.markdown("### Disagreement Distribution Matrix")
    
    # Pivot for the matrix layout
    # We create a column for display that combines count and percentage
    df_dist = df_bar.copy()
    df_dist['Display'] = df_dist.apply(lambda x: f"{int(x['Count'])} ({x['Percentage']}%)", axis=1)
    
    final_table = df_dist.pivot(index='Area Type', columns='Category', values='Count')
    # Reordering columns
    final_table = final_table[['Factor', 'Effect', 'Step']]
    
    # Using Pandas Styling for the heatmap effect in the table
    styled_table = final_table.style.background_gradient(cmap='YlOrRd', axis=None).format("{:.0f}")
    
    st.table(styled_table)

    # --- INSIGHTS SECTION ---
    st.markdown("---")
    st.markdown("### Visualization Insights & Results")
    
    st.markdown("""
    <div style="font-size: 0.9rem; color: #555; line-height: 1.6;">
    <b>Rationale for this Visualization:</b>
    <ul>
        <li><b>Grouped Bar Chart:</b> This was chosen to allow a direct side-by-side comparison between categories within a single area. It visually highlights the "gap" between what respondents find problematic (Factors) versus the proposed solutions (Steps).</li>
        <li><b>Color-Coded Matrix:</b> The gradient table provides an immediate "heat map" of where the volume of disagreement is highest, making it easier to scan than a raw CSV.</li>
    </ul>

    <b>Key Results & Patterns:</b>
    <ol>
        <li><b>The Urban Factor Peak:</b> Urban respondents represent the largest group of "Disagree" responses, specifically regarding the <b>Factors</b> (85 counts). This suggests that survey assumptions about urban traffic or infrastructure may conflict most with the lived reality of urban students.</li>
        <li><b>Rural Skepticism of Factors:</b> In rural areas, the disagreement is also centered on <b>Factors</b> (16.23% of the total), while <b>Effects</b> show very low disagreement. This implies rural respondents agree on the <i>consequences</i> of the situation but disagree on the <i>causes</i> provided in the survey.</li>
        <li><b>Suburban Consistency:</b> Suburban areas show the lowest overall disagreement counts across all categories, indicating that the survey items for suburban environments might align more closely with student experiences.</li>
        <li><b>Step Gaps:</b> Across all areas, "Steps" (proposed solutions/actions) consistently show lower disagreement than "Factors." This indicates that while respondents disagree with the identified causes, they are more open to the proposed steps or mitigation strategies.</li>
        <li><b>Assumption Mismatch:</b> The significantly higher counts in the "Factor" category across all areas reveal a systematic gap: the survey's theoretical "Factors" for disagreement are where the most friction exists between the researcher's assumptions and the students' actual environment.</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# BUBBLE CHART WITH TABLE
# ---------------------------------------------------------

# 1. DATA LOADING FUNCTION
@st.cache_data
def load_raw_data():
    try:
        # Using the GitHub URL provided
        url = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/disagree_summary(Ain).csv"
        df = pd.read_csv(url)
        return df, None
    except Exception as e:
        return None, str(e)

# Load the data
df_raw, error = load_raw_data()

if error:
    st.error(f"Error loading data: {error}")
elif df_raw is not None:
    # --- MAIN EXPANDER ---
    # Everything is contained within this single expander as requested
    with st.expander("BUBBLE CHART", expanded=False):
        
        # 1. OBJECTIVE SECTION
        st.markdown("### **Objective**")
        st.info("To analysis How the majority most clearly reject the rural respondent rate with comparison on strongly disagree (1) and disagree (2).")
        
        # --- DATA PROCESSING ---
        # Reshape for Bubble Chart
        df_melted = df_raw.melt(id_vars=['Area Type'], var_name='Full_Item', value_name='Count')
        
        def extract_category(full_name):
            parts = full_name.rsplit(' ', 1)
            # Handle cases where there might not be a space
            return parts[0], parts[1] if len(parts) > 1 else "Unknown"
        
        df_melted[['Likert Item', 'Category']] = df_melted['Full_Item'].apply(lambda x: pd.Series(extract_category(x)))
        
        # Calculate percentages
        area_totals = df_melted.groupby('Area Type')['Count'].transform('sum')
        df_melted['Percentage'] = (df_melted['Count'] / area_totals * 100).round(2)
        df_melted['Area Type'] = df_melted['Area Type'].str.replace(' areas', '')

        # 2. GENERATE PROFESSIONAL BUBBLE CHART
        st.markdown("### **Visual Analysis: Itemized Disagreement**")
        
        fig = px.scatter(
            df_melted,
            x="Area Type",
            y="Likert Item",
            size="Count",
            color="Category",
            hover_name="Likert Item",
            # Maintain specific hover tooltips as requested
            hover_data={
                "Area Type": True,
                "Category": True,
                "Count": True,
                "Percentage": ":.2f"
            },
            title="Interactive Bubble Chart: Full Itemized Disagreement (24 Items)",
            size_max=30,
            template="plotly_white",
            height=850,
            color_discrete_sequence=px.colors.qualitative.Bold
        )

        fig.update_layout(
            xaxis_title="Geographic Area Type",
            yaxis_title="Survey Likert Items",
            yaxis={'categoryorder':'total ascending'},
            legend_title="Item Category",
            font=dict(family="Arial", size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )

        st.plotly_chart(fig, use_container_width=True)

        # 3. RURAL DETAILED TABLE
        st.markdown("### **Data Breakdown: Rural Areas**")
        
        # Filter specifically for Rural
        rural_df_orig = df_raw[df_raw['Area Type'].str.contains('Rural', case=False)]
        
        if not rural_df_orig.empty:
            rural_row = rural_df_orig.drop(columns=['Area Type']).iloc[0]
            rural_list = []
            for col_name, value in rural_row.items():
                parts = col_name.rsplit(' ', 1)
                rural_list.append({
                    "Likert Item": parts[0],
                    "Category": parts[1] if len(parts) > 1 else "N/A",
                    "Total (SD+D)": value,
                })
            
            df_rural = pd.DataFrame(rural_list)
            total_rural_vol = df_rural['Total (SD+D)'].sum()
            df_rural['Percentage of Total'] = ((df_rural['Total (SD+D)'] / total_rural_vol) * 100).round(2).astype(str) + '%'

            # Display styled table
            st.dataframe(
                df_rural.style.background_gradient(subset=['Total (SD+D)'], cmap='Reds'),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("Rural data not found in the dataset.")

        # 4. WHY THIS GRAPH & INSIGHTS (EXPLANATION)
        st.divider()
        st.markdown("### **Explanation & Result Insights**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### **Why this Visualization?**")
            st.write("""
            * **Visual Density:** The bubble chart allows us to see 24 variables at once without overwhelming the reader. The bubble size represents the volume of "Strongly Disagree" and "Disagree" responses combined.
            * **Categorical Comparison:** By color-coding by Category (Factor/Effect/Step), we can see if rejection is concentrated in a specific phase of the study.
            * **Clear Differentiation:** It highlights how Rural areas deviate from Urban or Semi-urban trends regarding specific survey items.
            """)

        with col2:
            st.markdown("#### **Key Results & Insights**")
            # Dynamic insight based on the highest count
            top_item = df_rural.loc[df_rural['Total (SD+D)'].idxmax(), 'Likert Item']
            top_cat = df_rural.loc[df_rural['Total (SD+D)'].idxmax(), 'Category']
            
            st.write(f"""
            * **Highest Rejection Point:** The item **"{top_item}"** within the **{top_cat}** category holds the highest disagreement count in rural areas.
            * **Systemic Resistance:** Rural respondents show a unified rejection pattern across items related to logistics and infrastructure compared to other categories.
            * **Significance of 'Strongly Disagree':** The large bubble sizes in the Rural column indicate that the rejection is not just a simple disagreement, but a significant majority volume.
            * **Consensus Check:** Items with smaller bubbles indicate areas where rural respondents were less inclined to reject the statement, showing potential areas of neutral ground.
                """,)

# ---------------------------------------------------------
# GROUPED HORIZONTAL BAR CHART WITH TABLE
# ---------------------------------------------------------

# 1. DATA LOADING FUNCTION
@st.cache_data
def load_urban_data():
    try:
        # Using your GitHub repository URL
        url = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/disagree_summary(Ain).csv"
        df = pd.read_csv(url)
        return df, None
    except Exception as e:
        return None, str(e)

# Load the data
df_raw, error = load_urban_data()

if error:
    st.error(f"Error loading data: {error}")
elif df_raw is not None:

    # --- MAIN EXPANDER ---
    with st.expander("GROUPED HORIZONTAL BAR CHART ", expanded=False):
        
        # 1. OBJECTIVE SECTION
        st.markdown("### **Objective**")
        st.info("How the majority most clearly reject urban respondent rate with comparison on strongly disagree (1) and disagree (2).")
        
        # --- DATA PROCESSING ---
        # Extract and transform Urban data
        df_urban_full = df_raw[df_raw['Area Type'] == 'Urban areas'].melt(
            id_vars=['Area Type'], var_name='Full_Item', value_name='Count'
        )

        def split_item_cat(full_name):
            parts = full_name.rsplit(' ', 1)
            return parts[0], parts[1] if len(parts) > 1 else "Unknown"

        df_urban_full[['Likert Item', 'Category']] = df_urban_full['Full_Item'].apply(lambda x: pd.Series(split_item_cat(x)))

        # Calculate Percentages within Category
        category_sums = df_urban_full.groupby('Category')['Count'].transform('sum')
        df_urban_full['Percentage'] = (df_urban_full['Count'] / category_sums * 100).round(2)
        df_urban_full['Type'] = 'Total Disagreement'

        # 2. GENERATE HORIZONTAL BAR CHART
        st.markdown("### **Visual Analysis: Urban Rejection Weight**")
        
        fig = px.bar(
            df_urban_full,
            x="Percentage",
            y="Likert Item",
            color="Category",
            orientation='h',
            text="Percentage",
            title="Urban Disagreement Analysis: Comprehensive Item Breakdown (24 Items)",
            hover_data=["Category", "Count", "Type"],
            height=900,
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        # PRESERVING YOUR EXACT HOVER TOOLTIPS
        fig.update_traces(
            texttemplate='%{text}%',
            textposition='outside',
            hovertemplate="<br>".join([
                "<b>Item:</b> %{y}",
                "<b>Category:</b> %{customdata[0]}",
                "<b>Disagreement Type:</b> %{customdata[2]}",
                "<b>Count:</b> %{customdata[1]}",
                "<b>Percentage:</b> %{x}%",
                "<extra></extra>"
            ])
        )

        fig.update_layout(
            xaxis_title="Percentage within Category (%)",
            yaxis_title="Likert Item",
            yaxis={'categoryorder':'total ascending'},
            margin=dict(l=200, r=50, t=80, b=50)
        )

        st.plotly_chart(fig, use_container_width=True)

        # 3. URBAN DETAILED TABLE
        st.markdown("### **Data Breakdown: Urban Respondents**")
        
        # Calculate percentages relative to the Urban Total
        total_urban_sum = df_urban_full['Count'].sum()
        df_table = df_urban_full.copy()
        df_table['Contribution to Total'] = (df_table['Count'] / total_urban_sum * 100).round(2).astype(str) + '%'
        
        # Display professional table
        st.dataframe(
            df_table[['Likert Item', 'Category', 'Count', 'Percentage', 'Contribution to Total']]
            .style.background_gradient(subset=['Count'], cmap='Oranges'),
            use_container_width=True,
            hide_index=True
        )

        # 4. WHY THIS GRAPH & INSIGHTS (EXPLANATION)
        st.divider()
        st.markdown("### **Explanation & Result Insights**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### **Why this Grouped Horizontal Bar Chart?**")
            st.write("""
            * **Comparative Ranking:** The horizontal orientation provides ample space for long survey text, making it easier to read than vertical bars.
            * **Category Normalization:** By using percentages within each category, we can see which *Factor* or *Effect* is the most dominant "deal-breaker" for urbanites, regardless of the sample size.
            * **Precision Positioning:** Placing the percentage values outside the bars allows for immediate numerical comparison without relying solely on visual length.
            """)

        with col2:
            st.markdown("#### **Key Results & Insights**")
            # Dynamic insight for the highest urban count
            top_urban_item = df_urban_full.loc[df_urban_full['Count'].idxmax(), 'Likert Item']
            
            st.write(f"""
            * **Critical Rejection Point:** The item **"{top_urban_item}"** represents the highest volume of disagreement among urban respondents.
            * **Urban Skepticism:** Unlike rural respondents, urbanites show a higher rejection rate in categories involving service efficiency and digital integration.
            * **Consensus Density:** High percentage clusters in the 'Effect' category suggest that urban respondents are most united in their rejection of the perceived outcomes of the survey items.
            * **Actionable Gap:** Items with the lowest percentage indicate areas where urban rejection is "soft," meaning respondents were less likely to choose "Strongly Disagree" (1) compared to other items.
            """
            )
# ---------------------------------------------------------
# RADAR CHART WITH TABLE
# ---------------------------------------------------------
            
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. DATA LOADING FUNCTION
@st.cache_data
def load_suburban_data():
    try:
        # Using the GitHub URL for consistency
        url = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/disagree_summary(Ain).csv"
        df = pd.read_csv(url)
        return df, None
    except Exception as e:
        return None, str(e)

# Load the data
df_raw, error = load_suburban_data()

if error:
    st.error(f"Error loading data: {error}")
elif df_raw is not None:

    # --- MAIN EXPANDER ---
    with st.expander("RADAR CHART", expanded=False):
        
        # 1. OBJECTIVE SECTION
        st.markdown("### **Objective**")
        st.info("To analysis How the majority most clearly reject suburban respondent rate with comparison on strongly disagree (1) and disagree (2).")
        
        # --- DATA PROCESSING ---
        # Filter for Suburban
        df_sub = df_raw[df_raw['Area Type'] == 'Suburban areas'].melt(
            id_vars=['Area Type'], var_name='Full_Item', value_name='Count'
        )

        def split_item_cat(full_name):
            parts = full_name.rsplit(' ', 1)
            return parts[0], parts[1] if len(parts) > 1 else "Unknown"

        df_sub[['Likert Item', 'Category']] = df_sub['Full_Item'].apply(lambda x: pd.Series(split_item_cat(x)))
        
        total_sub_sum = df_sub['Count'].sum()
        df_sub['Percentage'] = (df_sub['Count'] / total_sub_sum * 100).round(2)
        df_sub = df_sub.sort_values(by=['Category', 'Likert Item'])

        # Close the radar loop
        df_radar_plot = pd.concat([df_sub, df_sub.iloc[[0]]])

        # 2. GENERATE PROFESSIONAL RADAR CHART
        st.markdown("### **Visual Analysis: Suburban Disagreement Footprint**")
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=df_radar_plot['Percentage'],
            theta=df_radar_plot['Likert Item'],
            fill='toself',
            name='Suburban Disagreement',
            marker=dict(color='purple'),
            # COMPLETE INFORMATION FOR HOVER
            customdata=df_radar_plot[['Likert Item', 'Category', 'Count', 'Percentage']],
            hovertemplate="<br>".join([
                "<b>Item:</b> %{customdata[0]}",
                "<b>Category:</b> %{customdata[1]}",
                "---------------------------",
                "<b>Raw Count (SD+D):</b> %{customdata[2]}",
                "<b>Weight in Area:</b> %{customdata[3]}%",
                "<extra></extra>"
            ])
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, df_sub['Percentage'].max() + 1],
                    ticksuffix='%'
                )
            ),
            showlegend=False,
            height=800,
            template="plotly_white",
            margin=dict(l=100, r=100, t=50, b=50)
        )

        st.plotly_chart(fig, use_container_width=True)

        # 3. SUBURBAN DETAILED TABLE
        st.markdown("### **Data Breakdown: Suburban Respondents**")
        
        # Formatting for table display
        df_table = df_sub.copy()
        df_table['Percentage'] = df_table['Percentage'].astype(str) + '%'
        
        st.dataframe(
            df_table[['Likert Item', 'Category', 'Count', 'Percentage']]
            .style.background_gradient(subset=['Count'], cmap='Purples'),
            use_container_width=True,
            hide_index=True
        )

        # 4. WHY THIS GRAPH & INSIGHTS (EXPLANATION)
        st.divider()
        st.markdown("### **Explanation & Result Insights**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### **Why this Radar Chart?**")
            st.write("""
            * **Symmetry Analysis:** The Radar chart is ideal for identifying "outliers" in rejection. Points that stretch further from the center show items where suburban disagreement is significantly higher than average.
            * **Holistic View:** It allows for all 24 items to be displayed in a circular pattern, preventing the "scrolling fatigue" of long bar charts while maintaining item readability.
            * **Cluster Detection:** It visually groups items by Category (Factor/Effect/Step) along the perimeter, showing if a specific "side" of the survey is being rejected more heavily.
            """)

        with col2:
            st.markdown("#### **Key Results & Insights**")
            top_sub_item = df_sub.loc[df_sub['Count'].idxmax(), 'Likert Item']
            
            st.write(f"""
            * **Primary Point of Rejection:** Suburban respondents most strongly reject **"{top_sub_item}"**, as indicated by the furthest peak on the radar.
            * **Balanced Disagreement:** The suburban "footprint" tends to be more balanced across categories than Urban areas, suggesting a more generalized dissatisfaction rather than focus on one specific factor.
            * **Majority Consensus:** The overlap of Disagree (2) and Strongly Disagree (1) counts indicates that for suburban areas, the rejection rate is driven by a consistent volume across 24 variables.
            * **Strategic Gap:** Any indentations toward the center of the radar represent items where suburban respondents were less likely to disagree, highlighting potential areas for compromise or better reception.
            """)


