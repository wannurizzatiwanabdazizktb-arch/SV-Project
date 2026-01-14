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
# --- 1. CONFIGURATION & DATA ---
# Ensure merged_df and column lists are defined before this block

with st.expander("Heatmap, and Stacked Bar", expanded=False):
    
    # --- OBJECTIVE SECTION ---
    st.markdown("""
    ### **Objective**
    Identify how respondents across **Rural, Suburban, and Urban** areas distribute their disagreements. 
    By analyzing the highest and lowest disagreement counts for **Factors, Effects, and Steps**, 
    we reveal the specific patterns and outliers within each Likert scale category.
    """)
    st.divider()

    # --- PART A: DATA PROCESSING ---
    heatmap_data_detailed = []
    for area in ['Rural areas', 'Suburban areas', 'Urban areas']:
        for col in all_likert_cols:
            count_sd = merged_df.loc[merged_df['Area Type'] == area, col].isin([1]).sum()
            count_d  = merged_df.loc[merged_df['Area Type'] == area, col].isin([2]).sum()
            total_dis = count_sd + count_d

            if total_dis >= 0: # Include 0s for complete pattern analysis
                heatmap_data_detailed.append({
                    'Area Type': area,
                    'Likert Item': col,
                    'Total Disagreement Count': total_dis,
                    'Strongly Disagree (1)': count_sd,
                    'Disagree (2)': count_d,
                    'Category': ('Factor' if col in factor_cols else 'Effect' if col in effect_cols else 'Step')
                })

    heatmap_df_detailed = pd.DataFrame(heatmap_data_detailed)

    # --- PART B: HEATMAP ---
    st.subheader("1. Disagreement Distribution Pattern")
    
    # Pivot and Reorder
    heatmap_pivot_z = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Total Disagreement Count').fillna(0)
    # Reorder index based on your categories
    item_order = [i for i in (factor_cols + effect_cols + step_cols) if i in heatmap_pivot_z.index]
    heatmap_pivot_z = heatmap_pivot_z.reindex(item_order)

    fig_heat = go.Figure(data=go.Heatmap(
        z=heatmap_pivot_z.values,
        x=heatmap_pivot_z.columns,
        y=heatmap_pivot_z.index,
        colorscale='YlGnBu',
        text=heatmap_pivot_z.values,
        texttemplate="%{text}",
        hovertemplate='<b>%{y}</b><br>Area: %{x}<br>Total Disagreement: %{z}<extra></extra>'
    ))
    fig_heat.update_layout(height=600, margin=dict(t=10, b=10), template='plotly_white')
    st.plotly_chart(fig_heat, use_container_width=True)

    st.divider()

    # --- PART C: BAR & STRUCTURED TABLE ---
    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        st.subheader("2. Overall Trend")
        bar_data = heatmap_df_detailed.groupby('Likert Item')['Total Disagreement Count'].sum().reset_index()
        bar_data = bar_data.sort_values('Total Disagreement Count', ascending=True)

        fig_bar = px.bar(bar_data, x='Total Disagreement Count', y='Likert Item', orientation='h',
                         color='Total Disagreement Count', color_continuous_scale='Viridis')
        fig_bar.update_layout(showlegend=False, height=500, margin=dict(l=150), template='plotly_white')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.subheader("3. Structured Key Insights")
        
        # Aggregate for insights
        summary = heatmap_df_detailed.groupby(['Likert Item', 'Category']).agg({
            'Total Disagreement Count': 'sum'
        }).reset_index()
        
        area_pivot = heatmap_df_detailed.pivot_table(
            index='Likert Item', columns='Area Type', values='Total Disagreement Count', fill_value=0
        ).reset_index()
        
        final_summary_df = summary.merge(area_pivot, on='Likert Item')

        # Create the specific "Top Factor, Bottom Factor..." structure
        structured_rows = []
        for cat in ['Factor', 'Effect', 'Step']:
            cat_data = final_summary_df[final_summary_df['Category'] == cat].sort_values('Total Disagreement Count', ascending=False)
            if not cat_data.empty:
                # Add a Label column to help the user
                top_row = cat_data.iloc[[0]].copy()
                top_row.insert(0, 'Rank', f'Highest {cat}')
                structured_rows.append(top_row)
                
                bottom_row = cat_data.iloc[[-1]].copy()
                bottom_row.insert(0, 'Rank', f'Lowest {cat}')
                structured_rows.append(bottom_row)

        if structured_rows:
            insight_table = pd.concat(structured_rows, ignore_index=True)
            st.dataframe(
                insight_table[['Rank', 'Likert Item', 'Total Disagreement Count', 'Rural areas', 'Suburban areas', 'Urban areas']],
                use_container_width=True, hide_index=True
            )
    
# --- FORMAL ANALYSIS & STRATEGIC INSIGHTS SECTION ---
    st.divider()
    
    # 1. METHODOLOGY JUSTIFICATION
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("""
        **Heatmap:**
        The heatmap effectively visualizes the **intensity and distribution** of disagreement across rural, suburban, and urban areas. It makes it easier to identify geographic concentration patterns, where darker shades immediately highlight items with stronger rejection in specific areas.
        """)
    with col_v2:
        st.markdown("""
        **Horizontal Bar Chart:**
        This allows **direct comparison** of total disagreement counts. It clearly ranks items from highest to lowest, supporting quick identification of dominant and minimal rejection patterns across the entire dataset.
        """)
    st.caption("Together, these visualizations show both magnitude (bar chart) and spatial distribution (heatmap) of disagreement.")

    st.divider()

    # 2. CATEGORICAL BREAKDOWN
    st.subheader("Categorical Analysis: Understanding Respondent Disagreement")

    # --- FACTOR ANALYSIS ---
    with st.container():
        st.markdown("### **1. Factor Analysis**")
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            st.error("**Highest Disagreement Factor** \n*Late Drop-off/Pick-up Factor* (Total = 22)")
            st.write("""
            **Why:** This factor shows strong disagreement particularly in urban areas (12), followed by rural (6) and suburban (4). This suggests that respondents, especially in urban settings, may not view late drop-offs or pick-ups as a major contributor to traffic congestion compared to structural issues like road capacity.
            """)
        with f_col2:
            st.success("**Lowest Disagreement Factor** \n*Narrow Road Factor* (Total = 5)")
            st.write("""
            **Why:** The low disagreement implies general acceptance that narrow roads contribute to congestion. Notably, disagreement is only observed in urban areas (5), while rural and suburban respondents show no disagreement, indicating consensus across most regions.
            """)

    # --- EFFECT ANALYSIS ---
    with st.container():
        st.markdown("### **2. Effect Analysis**")
        e_col1, e_col2 = st.columns(2)
        with e_col1:
            st.error("**Highest Disagreement Effect** \n*Unintended Road Accidents Effect* (Total = 11)")
            st.write("""
            **Why:** Most disagreement comes from urban respondents (9), suggesting that respondents may perceive accidents as sporadic events rather than consistent causes of congestion, especially in cities where congestion exists even without accidents.
            """)
        with e_col2:
            st.success("**Lowest Disagreement Effect** \n*Pressure on Road Users Effect* (Total = 2)")
            st.write("""
            **Why:** Very low disagreement across all areas indicates that respondents largely acknowledge pressure on road users as a valid effect of traffic congestion, making it one of the most accepted consequences.
            """)

    # --- STEP (SOLUTION) ANALYSIS ---
    with st.container():
        st.markdown("### **3. Step (Solution) Analysis**")
        s_col1, s_col2 = st.columns(2)
        with s_col1:
            st.error("**Highest Disagreement Step** \n*Vehicle Sharing Step* (Total = 14)")
            st.write("""
            **Why:** Disagreement is evenly split between rural (6) and urban (6) areas. This suggests resistance to vehicle sharing due to concerns such as convenience, accessibility, limited public transport integration, or cultural preference for private vehicles.
            """)
        with s_col2:
            st.success("**Lowest Disagreement Step** \n*Pedestrian Bridge Step* (Total = 2)")
            st.write("""
            **Why:** Minimal disagreement—only from urban respondents—indicates strong overall support. Respondents likely perceive pedestrian bridges as a practical and effective solution for reducing pedestrian-related traffic interruptions.
            """)

    st.divider()

    # 3. OVERALL CONCLUSION
    st.subheader("📌 Overall Conclusion")
    st.info("""
    Findings reveal that respondents selectively disagree with certain traffic-related factors, effects, and solutions rather than rejecting them uniformly:

    * **Resistance to Behavior:** Factors related to daily routines (late drop-off/pick-up) and behavioral change solutions (vehicle sharing) face the strongest resistance.
    * **Acceptance of Infrastructure:** Structural issues (narrow roads), human impact effects (pressure on road users), and physical infrastructure solutions (pedestrian bridges) show high acceptance.
    
    The combined use of heatmaps and horizontal bar charts successfully uncovers both ranking and spatial patterns of disagreement, supporting a deeper understanding of how perceptions differ across area types. These insights are valuable for policymakers when prioritizing traffic congestion interventions that align with public acceptance.
    """)
# ---------------------------------------------------------
# 5. Stacked Bar Chart 
# ---------------------------------------------------------

with st.expander("Stacked Bar chart", expanded=False):
    
    # --- OBJECTIVE SECTION ---
    st.markdown("""
    ### **Objective**
    Analyze how respondents from area type choose most disagreements (factors, effects, or step), 
    revealing gaps between real-world experiences and the survey’s assumptions.
    """)
    st.divider()

    # --- DATA FILTERING ---
    # Remove 'Special' category from the source dataframe for this analysis
    filtered_heatmap_df = heatmap_df[heatmap_df['Category'] != 'Special'].copy()

    # --- PART A: STACKED BAR CHART (Dark Professional Colors) ---
    dark_cat_color_map = {
        'Factor': '#1B4F72',  # Dark Blue
        'Effect': '#A04000',  # Dark Orange
        'Step': '#145A32',    # Dark Green
    }

    fig_stacked = px.bar(
        filtered_heatmap_df, 
        x='Area Type', 
        y='Total', 
        color='Category',
        title='Disagreement Counts (1 & 2) by Category and Area Type',
        labels={'Total': 'Number of Disagreements', 'Area Type': 'Area Type'},
        color_discrete_map=dark_cat_color_map,
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
    category_summary = filtered_heatmap_df.groupby('Category').agg({
        'Total': 'sum',
        'SD': 'sum',
        'D': 'sum'
    }).reset_index()

    area_pivot = filtered_heatmap_df.pivot_table(
        index='Category', 
        columns='Area Type', 
        values='Total', 
        aggfunc='sum'
    ).fillna(0).astype(int)

    final_cat_table = category_summary.merge(area_pivot, on='Category')
    final_cat_table = final_cat_table.rename(columns={
        'Total': 'Grand Total',
        'SD': 'Strongly Disagree (1)',
        'D': 'Disagree (2)'
    })
    st.dataframe(final_cat_table, use_container_width=True, hide_index=True)

    st.divider()

    # --- JUSTIFICATION SECTION ---
    st.markdown("""
    A **stacked bar chart** is selected because it allows simultaneous comparison across two dimensions
    This visualization is particularly effective for revealing which category accumulates the greatest rejection and where that rejection is most concentrated geographically.
    """)

    st.divider()

    # --- 1. FACTOR ANALYSIS (Soft Blue Highlight / Small Bold Subtitle) ---
    st.markdown("""
    #### <span style='background-color:#EBF5FB; color:#2E86C1; padding:3px 10px; border-radius:4px;'>**1. Factor Category (Highest Disagreement)**</span>
    """, unsafe_allow_html=True)
    
    st.write("""
    * **What** : The highest total disagreement count (112) among core categories, indicating that respondents most strongly reject the proposed causes of traffic congestion presented in the survey.

    * **Why** : This rejection is most pronounced in **urban areas (73)**, compared to rural (27) and suburban (12) areas, demonstrating a clear and distinct urban-driven trend. Urban respondents appear to disagree substantially with simplified or predefined congestion factors, suggesting that real-life traffic issues in cities are perceived as multifaceted, systemic, and context-dependent.
    """)

    # --- 2. EFFECT ANALYSIS (Soft Orange Highlight / Small Bold Subtitle) ---
    st.markdown("""
    ##### <span style='background-color:#FEF5E7; color:#D68910; padding:3px 10px; border-radius:4px;'>**2. Effect Category (Lowest Disagreement)**</span>
    """, unsafe_allow_html=True)
    
    st.write("""
    * **What** : The lowest level of disagreement (22) across core categories, with relatively low disagreement in urban (15), rural (5), and suburban (2) areas.

    * **Why** : This consistency indicates that respondents largely agree on the consequences of traffic congestion, regardless of where they live. The shared acceptance suggests that the impacts of congestion—such as time loss, stress, and reduced productivity—are universally experienced.
    """)

    # --- 3. STEP ANALYSIS (Soft Green Highlight / Small Bold Subtitle) ---
    st.markdown("""
    ###### <span style='background-color:#EAFAF1; color:#27AE60; padding:3px 10px; border-radius:4px;'>**3. Step Category (Moderate but Inconsistent Disagreement)**</span>
    """, unsafe_allow_html=True)
    
    st.write("""
    * **What** : Total disagreement (26) but displays notable variation across areas, with the highest disagreement in urban areas (14), followed by rural (9) and suburban (3).

    * **Why** : This pattern suggests uncertainty or skepticism toward the proposed solutions, particularly among urban respondents. In dense environments, suggested steps may be viewed as impractical or disconnected from real operational challenges.
    """)

    # --- FINAL CONCLUSION BLOCK ---
    st.divider()
    st.markdown("### 📌 **Overall Conclusion**")
    st.info("""
    In conclusion, the **Factor category is the most rejected**, followed by **Step**, while **Effect** receives the least disagreement. This hierarchy indicates that respondents agree on what traffic congestion causes (effects) but disagree with how the problem is defined (factors) and how it should be solved (steps).

    The findings highlight that real-life traffic experiences, particularly in urban areas, are more complex than the survey’s proposed assumptions.
    """)
# -----------------------------------------
# 6. BUBLE CHART [RURAL RESPONDEN SD VS D]
# --------------------------------------------
factor_cols = [
    'Rainy Weather Factor', 'Increasing Population Factor', 'Undisciplined Driver Factor',
    'Damaged Road Factor', 'Leaving Work Late Factor', 'Single Gate Factor',
    'Lack of Pedestrian Bridge Factor', 'Lack of Parking Space Factor', 
    'Late Drop-off/Pick-up Factor', 'Construction/Roadworks Factor', 'Narrow Road Factor'
]

effect_cols = [
    'Unintended Road Accidents Effect', 'Time Wastage Effect', 'Pressure on Road Users Effect', 
    'Students Late to School Effect', 'Environmental Pollution Effect', 'Fuel Wastage Effect'
]

step_cols = [
    'Widening Road Step', 'Vehicle Sharing Step', 'Two Gates Step', 'Arrive Early Step',
    'Special Drop-off Area Step', 'Pedestrian Bridge Step', 'Traffic Officers Step'
]

all_likert_cols = factor_cols + effect_cols + step_cols

# --- 2. DEFINE THE CLASSIFICATION FUNCTION ---
def classify_item(col):
    """Categorizes survey items based on the provided lists."""
    if col in factor_cols:
        return 'Factor'
    elif col in effect_cols:
        return 'Effect'
    elif col in step_cols:
        return 'Step'
    else:
        return 'Other'

with st.expander("Bubble Chart", expanded=False):
    
    # --- 1. PREPARE RURAL DATA ---
    rural_df = merged_df[merged_df['Area Type'] == 'Rural areas']
    rural_disagreement_data = []

    for col in all_likert_cols: # Use the combined list we defined earlier
        if col in rural_df.columns:
            count_sd = (rural_df[col] == 1).sum()
            count_d  = (rural_df[col] == 2).sum()
            
            cat = classify_item(col) # Using the function we defined earlier

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
        # --- 2. OBJECTIVE SECTION ---
        st.markdown("### **Objective**")
        st.write("To analyze how the majority most clearly reject the rural respondent rate with comparison on strongly disagree (1) and disagree (2).")
        st.divider()

        # --- 3. BUBBLE CHART ---
        df_bubble_rural = df_bubble_rural.sort_values(['Category', 'Count'])

        fig_bubble = px.scatter(
            df_bubble_rural,
            x='Count',
            y='Likert Item',
            size='Count',
            color='Level',
            # UPDATED TO SOFT BLUE AND SOFT GREEN
            color_discrete_map={'Strongly Disagree (1)':'#85C1E9','Disagree (2)':'#82E0AA'}, 
            hover_name='Likert Item',
            hover_data={'Level':True, 'Count':True, 'Category':True},
            size_max=30,
            height=600,
            template='plotly_white',
            title='<b>Disagreement Intensity (Rural Respondents)</b>'
        )
        
        fig_bubble.update_layout(
            xaxis_title='Number of Responses',
            yaxis_title='Likert Scale Item',
            legend_title_text='Disagreement Level'
        )
        
        st.plotly_chart(fig_bubble, use_container_width=True)

        # --- 4. RURAL SUMMARY TABLE ---
        st.divider()
        st.subheader("2. Rural Disagreement Summary Table")
        
        rural_table = df_bubble_rural.pivot_table(
            index=['Category', 'Likert Item'], 
            columns='Level', 
            values='Count', 
            aggfunc='sum'
        ).fillna(0).reset_index()

        st.dataframe(rural_table, use_container_width=True, hide_index=True)

        # --- 5. INTERPRETATION (NOW PROPERLY INDENTED) ---
        st.divider()
        st.info("""
        **Why Use a Bubble Chart?** : The size of the bubble represents the volume of disagreement, making the most rejected items immediately stand out. 
        It allows us to see how 'Factor', 'Effect', and 'Step' intensity differs across the two Likert levels (1 vs 2) in a single view.
        """)

        # 1. Strongly Disagree Section
        st.markdown("""
        <div style="background-color:#EBF5FB; padding:20px; border-radius:10px; border-left: 5px solid #2E86C1; margin-bottom: 20px;">
            <h4 style="color:#2E86C1; margin-top:0;">Analysis of Strongly Disagree (1)</h4>
            <p>It is clear from the data visualization that Strongly Disagree (1) responses are more visible, expressing sharp rejection of alleged congestion factors.</p>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 5px;"><strong>What</strong> : Lower traffic volume in rural areas, <strong>"Late Drop-off/Pick-up Factor"</strong> displays the strongest number of disapproval responses (5).</li>
                <li style="margin-bottom: 10px;"><strong>Why</strong> : Meaning rural residents do not believe school-related activities significantly contribute to congestion.</li>
                <hr style="border: 0.5px solid #AED6F1; margin: 15px 0;">
                <li style="margin-bottom: 5px;"><strong>What</strong> : Strong disagreement is also measured for the <strong>"Environmental Pollution Effect" (1)</strong> and <strong>"Special Drop-off Areas Step" (1)</strong>.</li>
                <li><strong>Why</strong> : Rural respondents are likely unconvinced of a strong link between traffic and pollution because vehicular flow in their areas is much smoother than in urban settings.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # 2. Disagree Section
        st.markdown("""
        <div style="background-color:#EAFAF1; padding:20px; border-radius:10px; border-left: 5px solid #27AE60;">
            <h4 style="color:#27AE60; margin-top:0;">Analysis of Disagree (2)</h4>
            <p>Responses under "Disagree (2)" are less common but reveal slight skepticism.</p>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 5px;"><strong>What</strong> : The <strong>“Increasing Population Factor” (2)</strong> received the maximum number of disagreements in this category.</li>
                <li style="margin-bottom: 10px;"><strong>Why</strong> : While rural residents acknowledge population growth, they do not rate it as a serious cause of traffic problems.</li>
                <hr style="border: 0.5px solid #ABEBC6; margin: 15px 0;">
                <li style="margin-bottom: 5px;"><strong>What</strong> : Similarly, the rejection of <strong>“Students Late to School Effect” (1)</strong> confirms that rural life is not closely related to urban traffic pressures.</li>
                <li><strong>Why</strong> : Rural areas typically have less centralized congestion, meaning travel times for students are more predictable than in cities.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # 3. Conclusion for Rural Section
        st.success("""
        **Summary of Rural Perspective:** Rural respondents tend to lean further toward **Strongly Disagree (1)** than to "Disagree (2)," especially regarding behavioral variables. Ambiguity exists where responses for both levels are equal, likely due to varying local road scenarios, but the overall trend shows a firm rejection of urban-centric traffic assumptions.
        """)
    else:
        st.write("No disagreement data found for Rural areas.")
# --------------------------------------------        
# GROUP HORIZONTAL BAR CHART [URBAN SD VS D]
# --------------------------------------------
# --- 1. DEFINE YOUR COLUMN LISTS ---
factor_cols = [
    'Rainy Weather Factor', 'Increasing Population Factor', 'Undisciplined Driver Factor',
    'Damaged Road Factor', 'Leaving Work Late Factor', 'Single Gate Factor',
    'Lack of Pedestrian Bridge Factor', 'Lack of Parking Space Factor', 
    'Late Drop-off/Pick-up Factor', 'Construction/Roadworks Factor', 'Narrow Road Factor'
]

effect_cols = [
    'Unintended Road Accidents Effect', 'Time Wastage Effect', 'Pressure on Road Users Effect', 
    'Students Late to School Effect', 'Environmental Pollution Effect', 'Fuel Wastage Effect'
]

step_cols = [
    'Widening Road Step', 'Vehicle Sharing Step', 'Two Gates Step', 'Arrive Early Step',
    'Special Drop-off Area Step', 'Pedestrian Bridge Step', 'Traffic Officers Step'
]

all_likert_cols = factor_cols + effect_cols + step_cols

# --- 2. DEFINE THE CLASSIFICATION FUNCTION ---
def classify_item(col):
    """Categorizes survey items based on the provided lists."""
    if col in factor_cols:
        return 'Factor'
    elif col in effect_cols:
        return 'Effect'
    elif col in step_cols:
        return 'Step'
    else:
        return 'Other'

# --- 3. URBAN EXPANDER ---
with st.expander("Group Horizontal Bar Chart", expanded=False):
    # Filter for Urban respondents
    urban_df = merged_df[merged_df['Area Type'] == 'Urban areas']
    
    disagreement_data = []
    for col in all_likert_cols:
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

        # --- OBJECTIVE ---
        st.markdown("### **Objective**")
        st.write("""
        This analysis investigates how the majority most clearly reject urban respondent rate with 
        comparison on strongly disagree (1) and disagree (2).
        """)
        st.divider()

        # --- PART A: GROUPED BAR CHART ---
        fig = go.Figure()

        # Strongly Disagree Trace (Dark Blue)
        fig.add_trace(go.Bar(
            y=disagreement_df['Likert Scale Item'],
            x=disagreement_df['Strongly Disagree (1)'],
            orientation='h',
            name='Strongly Disagree (1)',
            marker=dict(color='#85C1E9'),
            customdata=disagreement_df[['Item Category', 'Strongly Disagree (1)']],
            hovertemplate=(
                '<b>Likert Scale Item:</b> %{y}<br>' +
                '<b>Item Category:</b> %{customdata[0]}<br>' +
                '<b>Disagreement Level:</b> Strongly Disagree (1)<br>' +
                '<b>Number of Disagreement Responses:</b> %{customdata[1]}<extra></extra>'
            )
        ))

        # Disagree Trace (Dark Green)
        fig.add_trace(go.Bar(
            y=disagreement_df['Likert Scale Item'],
            x=disagreement_df['Disagree (2)'],
            orientation='h',
            name='Disagree (2)',
            marker=dict(color='#145A32'),
            customdata=disagreement_df[['Item Category', 'Disagree (2)']],
            hovertemplate=(
                '<b>Likert Scale Item:</b> %{y}<br>' +
                '<b>Item Category:</b> %{customdata[0]}<br>' +
                '<b>Disagreement Level:</b> Disagree (2)<br>' +
                '<b>Number of Disagreement Responses:</b> %{customdata[1]}<extra></extra>'
            )
        ))

        fig.update_layout(
            title='<b>Disagreement Responses (1 vs 2) among Urban Respondents</b>',
            title_font_size=20,
            barmode='group',
            xaxis_title='Number of Responses',
            yaxis_title='Likert Scale Item',
            legend_title_text='Disagreement Level',
            template='plotly_white',
            height=800,
            margin=dict(l=250, t=80)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # --- PART B: SUMMARY TABLE ---
        st.markdown("### **Urban Disagreement Summary Table**")
        st.dataframe(disagreement_df[['Likert Scale Item', 'Item Category', 'Strongly Disagree (1)', 'Disagree (2)']], 
                     use_container_width=True, hide_index=True)

        st.divider()

        # --- PART C:INTERPRETATION ---
        st.write("""
        **Why Use a Grouped Horizontal Bar Chart?** This chart provides a side-by-side comparison of the intensity of rejection. 
        Horizontal orientation is utilized to ensure that long survey item labels remain readable, while grouping allows 
        to see at a glance whether respondents are 'Strongly' rejecting a point or simply 'Disagreeing'.
        """)

        # Analysis of Strongly Disagree (1)
        st.markdown("""
        #### <span style='background-color:#EBF5FB; color:#2E86C1; padding:3px 10px; border-radius:4px;'>**Analysis of Strongly Disagree (1)**</span>
        """, unsafe_allow_html=True)
        st.write("""
        The visualization reveals that **‘Strongly Disagree (1)’** has a notable level of disagreement with various behavioral and structural theories of traffic congestion. 
        * **What** :  The "Single Gate Factor" records the highest level of strong disagreement (9) on the scale. 
        * **Why** : Respondents do not believe a single gate significantly contributes to traffic congestion, as they see congestion as mainly caused by higher traffic volume and road conditions rather than access points.
        """)

        # Analysis of Disagree (2)
        st.markdown("""
        #### <span style='background-color:#EAFAF1; color:#27AE60; padding:3px 10px; border-radius:4px;'>**Analysis of Disagree (2)**</span>
        """, unsafe_allow_html=True)
        st.write("""
        The **‘Disagree (2)’** responses tend to be relatively high on most of the questions, reflecting a considerable but widespread level of disapproval. 
        * **What** : Items like "Leaving Work Factor" and " Unintended Road Accidents Effect" are records the same highest level of disagreement (7)
        * **Why** : Reflecting their ambivalence to the fact that they do not regard these factors as primary contributors to traffic congestion in cities.
        """)

        # --- BEAUTIFUL SUMMARY BLOCK ---
        st.divider()
        st.markdown("### **Summary of Urban Sentiment**")
        st.success("""
        Urban respondents act as the most active "skeptics" (Disagreement) of the survey. 
        While they strongly reject structural assumptions (like Single Gates), their general trend leans toward Disagree (2). 
        This indicates that for urbanites, traffic is an ambiguous and multifaceted issue where predefined causes and solutions 
        are often viewed as insufficient or out of touch with the systemic nature of city congestion.
        """)

    else:
        st.warning("No disagreement data found for Urban areas.")
# -----------------------------------------
# RADAR CHART  [ SUBURBAN ANALYSIS SD VS D
# ------------------------------------------
with st.expander("Radar Chart", expanded=False):
    
# Filter for Suburban respondents
    suburban_df = merged_df[merged_df['Area Type'] == 'Suburban areas']

    # Prepare disagreement data
    sub_dis_data = []
    for col in all_likert_cols:
        # Skip outliers as per your logic
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
        # --- OBJECTIVE SECTION ---
        st.markdown("### **Objective**")
        st.write("""
        Analyze how the majority most clearly reject suburban respondent 
        rate with comparison on strongly disagree (1) and disagree (2).
        """)
        st.divider()
        
        # Melt data for radar chart compatibility
        sub_melted = df_suburban.melt(
            id_vars=['Likert Item','Category'],
            value_vars=['Strongly Disagree (1)','Disagree (2)'],
            var_name='Disagreement Type',
            value_name='Total Disagreement'
        )

        # --- PART A: RADAR CHART ---
        # Create radar chart with detailed Hover Template
        fig_radar = px.line_polar(
            sub_melted,
            r='Total Disagreement',
            theta='Likert Item',
            color='Disagreement Type',
            line_close=True,
            markers=True,
            title='<b>Disagreement Responses (1 vs 2) among Suburban Respondents</b>',
            color_discrete_map={'Strongly Disagree (1)':'#1B4F72','Disagree (2)':'#145A32'},
            template='plotly_white'
        )

        # Detailed Hover Configuration
        fig_radar.update_traces(
            hovertemplate="<b>Item:</b> %{theta}<br>" +
                          "<b>Category:</b> %{customdata[0]}<br>" +
                          "<b>Type:</b> %{fullData.name}<br>" +
                          "<b>Count:</b> %{r}<extra></extra>",
            customdata=sub_melted[['Category']]
        )

        fig_radar.update_layout(
            title_font_size=20,
            polar=dict(
                radialaxis=dict(
                    title='Response Count', 
                    visible=True, 
                    tickfont_size=10,
                    gridcolor="#E5E7E9"
                ),
                angularaxis=dict(
                    tickfont_size=10,
                    gridcolor="#E5E7E9"
                ),
                bgcolor="rgba(255,255,255,0)"
            ),
            height=700,
            margin=dict(t=100, b=100, l=50, r=50),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(fig_radar, use_container_width=True)

        st.divider()

        # --- PART B: SUMMARY TABLE ---
        st.markdown("### **Suburban Disagreement Summary Table**")
        st.dataframe(
            df_suburban[['Likert Item', 'Category', 'Strongly Disagree (1)', 'Disagree (2)']], 
            use_container_width=True, 
            hide_index=True
        )

        st.divider()
        st.write("""
        **Why Use a Radar Chart?** A radar chart (or spider chart) is selected for the suburban analysis to visualize the 
        disagreement type count with comparison. It allows to see which specific survey dimensions are pulling 
        the most weight, identifying whether the disagreement is balanced or skewed toward specific items.
        """)

        # Analysis of Strongly Disagree (1)
        st.markdown("""
        #### <span style='background-color:#EBF5FB; color:#2E86C1; padding:3px 10px; border-radius:4px;'>**Analysis of Strongly Disagree (1)**</span>
        """, unsafe_allow_html=True)
        st.write("""
        * **What** : The item "Vehicle Sharing Step" (2) stands out with the greatest number of strong rejections. 
        * **Why** : This data clearly demonstrates that suburban respondents strongly dislike car-sharing as a proposed solution to alleviate traffic problems. 
        """)

        # Analysis of Disagree (2)
        st.markdown("""
        #### <span style='background-color:#EAFAF1; color:#27AE60; padding:3px 10px; border-radius:4px;'>**Analysis of Disagree (2)**</span>
        """, unsafe_allow_html=True)
        
        st.write("""
        * **What** :  The “Late Drop-off/Pick-up Factor” (3), represent the highest volume of disagreement in this area. 
        * **Why** : This pattern suggests that while suburban participants may not feel the need to "outright deny" these factors, they do not consider them to be major or relevant causes of traffic congestion in their specific neighborhoods.
        """)

        st.divider()
        st.markdown("## **Summary of Suburban Sentiment**")
        
        st.info("""
        The Disagree (2) category shows higher frequencies than Strongly Disagree (1), indicating weaker rather than strong rejection.
        """)

    else:
        st.info("No disagreement data found for Suburban areas (excluding outliers).")
