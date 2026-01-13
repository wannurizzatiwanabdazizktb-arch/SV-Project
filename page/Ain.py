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

# Combine all lists into one for the loop
all_likert_cols = factor_cols + effect_cols + step_cols

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

with st.expander("Heatmap and Horizontal Bar Chart", expanded=False):
    
    # --- OBJECTIVE SECTION ---
    st.markdown("""
    ### **Objective**
    Identify How respondents from all area types choose most and lowest disagreements items 
    (factors, effects, and step), to reveal the pattern of each Likert scale item count.
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
        bar_data = heatmap_df_detailed.groupby('Likert Item')['Total Disagreement Count'].sum().reset_index()
        bar_data = bar_data.sort_values('Total Disagreement Count', ascending=True)

        fig_bar = px.bar(bar_data, x='Total Disagreement Count', y='Likert Item', orientation='h',
                         color='Total Disagreement Count', color_continuous_scale='Viridis')
        fig_bar.update_layout(showlegend=False, height=500, margin=dict(l=150), template='plotly_white')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
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
    st.subheader("Why Use a Heatmap and Horizontal Bar Chart")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("""
        **Heatmap:**
        The heatmap effectively visualizes the intensity and distribution of disagreement across rural, suburban, and urban areas. It makes it easier to identify geographic concentration patterns, where darker shades immediately highlight items with stronger rejection in specific areas.
        """)
    with col_v2:
        st.markdown("""
        **Horizontal Bar Chart:**
        This allows direct comparison of total disagreement counts. It clearly ranks items from highest to lowest, supporting quick identification of dominant and minimal rejection patterns across the entire dataset.
        """)
    st.caption("Together, these visualizations show both magnitude (bar chart) and spatial distribution (heatmap) of disagreement.")

    st.divider()

    # 2. CATEGORICAL BREAKDOWN
    st.subheader("Understanding Respondent Disagreement")

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
        st.markdown("### **3. Step Analysis**")
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
    st.subheader("Conclusion")
    st.info("""
    Findings reveal that respondents selectively disagree with certain traffic-related factors, effects, and solutions rather than rejecting them uniformly:

    * Resistance to Behavior: Factors related to daily routines (late drop-off/pick-up) and behavioral change solutions (vehicle sharing) face the strongest resistance.
    * Acceptance of Infrastructure: Structural issues (narrow roads), human impact effects (pressure on road users), and physical infrastructure solutions (pedestrian bridges) show high acceptance.
    
    The combined use of heatmaps and horizontal bar charts successfully uncovers both ranking and spatial patterns of disagreement, supporting a deeper understanding of how perceptions differ across area types. These insights are valuable for policymakers when prioritizing traffic congestion interventions that align with public acceptance.
    """)
# ---------------------------------------------------------
# 5. Stacked Bar Chart with Table & Insight
# ---------------------------------------------------------
with st.expander("Stacked Bar Chart", expanded=False):
    
    # --- OBJECTIVE SECTION ---
    st.markdown("""
    ### **Objective**
    Analyze how respondents from area type choose most disagreements (factors, effects, or step), 
    revealing gaps between real-world experiences and the survey’s assumptions.
    """)
    st.divider()

    # --- PART A: STACKED BAR CHART ---
    # Ensure column names match your dataframe (assuming 'Total', 'SD', 'D' from your prompt)
    fig_stacked = px.bar(
        heatmap_df, 
        x='Area Type', 
        y='Total', 
        color='Category',
        title='Stacked Disagreement Responses by Category',
        labels={'Total': 'Number of Disagreements', 'Area Type': 'Area Type'},
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
    
    category_summary = heatmap_df.groupby('Category').agg({
        'Total': 'sum',
        'SD': 'sum',
        'D': 'sum'
    }).reset_index()

    area_pivot = heatmap_df.pivot_table(
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

    st.write("Consolidated disagreement counts across all survey categories:")
    st.dataframe(final_cat_table, use_container_width=True, hide_index=True)

# --- PART C: INSIGHT ANALYSIS BY CATEGORY ---
    st.divider()
    st.subheader("📝 Insight Analysis by Category")

    # Factor Analysis
    with st.container():
        st.markdown("#### **1. Factor: The 'Conceptual Gap'**")
        st.write("""
        The **'Factor'** category received the highest level of disagreement (130), with Urban areas (85) being the most vocal.
        
        * **The Gap:** This suggests the survey likely proposed "textbook" causes for traffic. Urbanites, who live in the congestion daily, clearly feel these factors are incorrect or oversimplified.
        * **Reasoning:** To an urban resident, congestion is likely seen as a systemic or structural failure (bad light timing, poor transit integration) rather than the simple factors suggested by the survey designer.
        """)

    # Step Analysis
    with st.container():
        st.markdown("#### **2. Step: The 'Practicality Gap'**")
        st.write("""
        **'Step'** shows a significant level of disagreement, especially in Urban (17) and Rural (11) areas.
        
        * **The Gap:** When respondents disagree with a "Step," they are rejecting a solution.
        * **Reasoning:** In Urban areas, proposed steps might be seen as impractical (e.g., "use a bike" in a city with no bike lanes). In Rural areas, the steps might be seen as irrelevant. This inconsistency shows the survey's solutions aren't "one size fits all."
        """)

    # Effect Analysis
    with st.container():
        st.markdown("#### **3. Effect: The 'Common Ground'**")
        st.write("""
        This category has the lowest disagreement (30).
        
        * **The Gap:** There is very little gap here. Almost everyone—regardless of where they live—agrees on what the results of traffic are (e.g., lost time, stress, pollution).
        * **Reasoning:** While people disagree on *why* traffic happens (Factor) or *how* to fix it (Step), they are united in the shared experience of the pain it causes.
        """)

    # --- SUMMARY OF FINDINGS & FINAL CONCLUSION ---
    st.divider()
    st.subheader("📌 Summary of Findings")
    st.write("""
    The survey reveals a **'Top-Down' vs. 'Bottom-Up'** disconnect:
    1.  **Factor (Highest Rejection):** The survey's understanding of why traffic happens is the furthest from reality for the respondents.
    2.  **Step (Moderate Rejection):** The survey's solutions are viewed as insufficient or out of touch with local needs.
    3.  **Effect (Lowest Rejection):** The survey accurately identifies the consequences of traffic.
    """)

    st.success("""
    **Conclusion:** To improve the survey's relevance, authors should focus on re-evaluating the **Factors**, as this is where the largest intellectual gap exists between the researchers and the people living in the urban environment.
    """)
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
