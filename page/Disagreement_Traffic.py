# =========================================================
# Traffic Congestion Survey Analysis of Disagreement Likert Scale
# Enhanced Version — by Nurul Ain Maisarah Hamidin (2026)
# =========================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. PAGE SETTINGS (Must be the first Streamlit command)
st.set_page_config(
    page_title="Traffic Congestion Survey Analysis",
    page_icon="📊",
    layout="wide"
)

# 2. LOAD DATA
@st.cache_data
def load_data():
    # Ensure this file exists in your directory
    return pd.read_csv("cleaned_data.csv")

try:
    merged_df = load_data()
except FileNotFoundError:
    st.error("CSV file not found. Please ensure 'cleaned_data.csv' is in the folder.")
    st.stop()

# 3. DEFINE COLUMNS & CATEGORIES
# Adjust indices [3:10] based on your actual CSV structure
likert_cols = merged_df.columns[3:28].tolist() 
factor_cols = [col for col in likert_cols if 'Factor' in col]
effect_cols = [col for col in likert_cols if 'Effect' in col]
step_cols   = [col for col in likert_cols if 'Step' in col]

# 4. DEFINE COLUMNS & CATEGORIES
# Assuming merged_df and likert_cols are already defined

result_original = {}

for col in likert_cols:
    result_original[col] = (
        merged_df[merged_df[col].isin([1, 2])]
        .groupby('Area Type')[col]
        .count()
    )

# Create the DataFrame and fill missing values
disagree_area_type_original = pd.DataFrame(result_original).fillna(0).astype(int)

# --- Streamlit Display Section ---

st.title("Disagreement (Likert 1–2) responses regarding traffic-related factors, effects, and steps across Area Types ")

# Option 1: Interactive Table (Allows sorting and resizing)
st.dataframe(disagree_area_type_original, use_container_width=True)

# Option 2: Static Table (Better for simple, non-interactive reports)
# st.table(disagree_area_type_original)

# ---------------------------------------------------------
# KPI METRICS (INTERPRETIVE SUMMARY BOX)
# ---------------------------------------------------------

st.subheader(
    "How respondents from all area types choose most disagreements (factors, effects, and step), "
    "to reveal the pattern of each Likert scale item count."
)
st.markdown("## Most higly Disagreement Insights by Category")

col1, col2, col3, col4 = st.columns(4)

# ---- COL 1: FACTOR ----
col1.metric(
    label="Most Disagreement Factor",
    value="33",
    help=(
        "Students Not Sharing Vehicles. "
        "Rural areas (9), "
        "Suburban areas (6), "
        "Urban areas (18). "
        "Disagree (20) and Strongly Disagree (13). "
    )
)

# ---- COL 2: EFFECT ----
col2.metric(
    label="Most Disagreement Effect",
    value="11",
    help=(
        "Unintended Road Accidents Effect. "
        "Rural areas (1), "
        "Suburban areas (1), " 
        "Urban areas (9). "
        "Disagree (9) and Strongly Disagree (2). "
    )
)

# ---- COL 3: STEP ----
col3.metric(
    label="Most Disagreement Step",
    value="14",
    help=(
        "Vehicle Sharing Step, "
        "Rural areas (6), "
        "Suburban areas (2), " 
        "Urban areas (6). "
        "Disagree (8) and Strongly Disagree (6). "
    )
)

# ---- COL 4: OVERALL CONCLUSION ----
col4.metric(
    label="Lowest Disagreement Item",
    value="2",
    help=(
        "Pressure on Road User Effect, "
        "Rural areas (1), "
        "Suburban areas (0), " 
        "Urban areas (1). "
        "Disagree (1) and Strongly Disagree (1). "
    )
)

st.markdown("---")

# ---------------------------------------------------------
# MODULE 1: HEATMAP & OVERALL DISAGREEMENT
# ---------------------------------------------------------
# How respondents from all area type choose most disagreements (factors, effects, and step), to reveal the pattern of each Likert scale item count.
# --- Data Processing (Same as your logic) ---

heatmap_data_detailed = []

# Define your categories (assumed to be pre-defined)
# likert_cols, factor_cols, effect_cols, step_cols = [...] 

for area in ['Rural areas', 'Suburban areas', 'Urban areas']:
    for col in likert_cols:
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
                'Category': ('Factor' if col in factor_cols else 'Effect' if col in effect_cols else 'Step')
            })

heatmap_df_detailed = pd.DataFrame(heatmap_data_detailed)

# Sorting and Pivoting
item_order = (
    heatmap_df_detailed[heatmap_df_detailed['Category']=='Factor']['Likert Item'].unique().tolist() +
    heatmap_df_detailed[heatmap_df_detailed['Category']=='Effect']['Likert Item'].unique().tolist() +
    heatmap_df_detailed[heatmap_df_detailed['Category']=='Step']['Likert Item'].unique().tolist()
)
heatmap_df_detailed['Likert Item'] = pd.Categorical(heatmap_df_detailed['Likert Item'], categories=item_order, ordered=True)

heatmap_pivot_z = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Total Disagreement Count').fillna(0)
heatmap_pivot_sd = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Strongly Disagree (1)').fillna(0)
heatmap_pivot_d = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Disagree (2)').fillna(0)

# Build CustomData Array
customdata_array = []
for likert_item in heatmap_pivot_z.index:
    row_data = []
    for area_type in heatmap_pivot_z.columns:
        sd_val = heatmap_pivot_sd.loc[likert_item, area_type] if area_type in heatmap_pivot_sd.columns else 0
        d_val = heatmap_pivot_d.loc[likert_item, area_type] if area_type in heatmap_pivot_d.columns else 0
        row_data.append([sd_val, d_val])
    customdata_array.append(row_data)

customdata_array = np.array(customdata_array)

# --- Create Plotly Figure ---

fig = go.Figure(data=go.Heatmap(
    z=heatmap_pivot_z.values,
    x=heatmap_pivot_z.columns,
    y=heatmap_pivot_z.index,
    colorscale='YlGnBu',
    text=heatmap_pivot_z.values,
    texttemplate="%{text}",
    showscale=True,
    hovertemplate='<b>%{y}</b><br>Area: %{x}<br>Total Disagreement: %{z}<br>Strongly Disagree (1): %{customdata[0]}<br>Disagree (2): %{customdata[1]}<extra></extra>',
    customdata=customdata_array
))

# Add grid lines
for i in range(len(heatmap_pivot_z.index)+1):
    fig.add_shape(type='line', x0=-0.5, x1=len(heatmap_pivot_z.columns)-0.5, y0=i-0.5, y1=i-0.5, line=dict(color='white', width=2))
for j in range(len(heatmap_pivot_z.columns)+1):
    fig.add_shape(type='line', y0=-0.5, y1=len(heatmap_pivot_z.index)-0.5, x0=j-0.5, x1=j-0.5, line=dict(color='white', width=2))

fig.update_layout(
    title="Disagreement Responses (1 & 2) Across Area Types on All Category",
    xaxis_title="Area Type",
    yaxis_title="Likert Scale Item",
    template='plotly_white',
    height=900
)

# --- Streamlit Display ---

st.title("Disagreement Heatmap Analysis")
st.plotly_chart(fig, use_container_width=True)
# ---------------------------------------------------------
# MODULE 2: BAR CHART ANALYSIS
# ---------------------------------------------------------
# 1. Prepare the Data
data = {
    'Likert Item': [
        'Rainy Weather Factor', 'Increasing Population Factor', 'Undisciplined Driver Factor',
        'Damaged Road Factor', 'Leaving Work Late Factor', 'Single Gate Factor',
        'Lack of Pedestrian Bridge Factor', 'Lack of Parking Space Factor', 'Late Drop-off/Pick-up Factor',
        'Construction/Roadworks Factor', 'Narrow Road Factor', 'Unintended Road Accidents Effect',
        'Time Wastage Effect', 'Pressure on Road Users Effect', 'Students Late to School Effect',
        'Environmental Pollution Effect', 'Fuel Wastage Effect', 'Students Not Sharing Vehicles',
        'Widening Road Step', 'Vehicle Sharing Step', 'Two Gates Step', 'Arrive Early Step',
        'Special Drop-off Area Step', 'Pedestrian Bridge Step', 'Traffic Officers Step'
    ],
    'Rural areas': [
        2.0, 2.0, 2.0, 2.0, 5.0, 6.0, 2.0, 2.0, 6.0, 2.0, 0.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 9.0, 1.0, 6.0, 1.0, 2.0, 1.0, 0.0, 0.0
    ],
    'Suburban areas': [
        0.0, 2.0, 2.0, 1.0, 2.0, 1.0, 1.0, 0.0, 4.0, 1.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 1.0, 1.0, 6.0, 0.0, 2.0, 0.0, 1.0, 0.0, 0.0, 0.0
    ],
    'Urban areas': [
        6.0, 6.0, 5.0, 6.0, 10.0, 14.0, 7.0, 7.0, 12.0, 7.0, 5.0, 9.0, 2.0,
        1.0, 2.0, 1.0, 6.0, 18.0, 1.0, 6.0, 2.0, 2.0, 2.0, 2.0, 2.0
    ],
    'Total Disagreement Count': [
        8.0, 10.0, 9.0, 9.0, 17.0, 21.0, 10.0, 9.0, 22.0, 10.0, 5.0, 11.0, 3.0,
        2.0, 3.0, 3.0, 8.0, 33.0, 2.0, 14.0, 3.0, 5.0, 3.0, 2.0, 2.0
    ]
}
disagreement_summary_df = pd.DataFrame(data)

# 2. Sort the Data
disagreement_summary_df_sorted = disagreement_summary_df.sort_values(
    'Total Disagreement Count', ascending=True
)

# 3. Create Plotly Figure
fig = px.bar(
    disagreement_summary_df_sorted,
    x='Total Disagreement Count',
    y='Likert Item',
    orientation='h',
    title='Total Disagreement Counts (1 & 2) for Each Likert Item Across All Area Types',
    labels={
        'Total Disagreement Count': 'Total Number of Disagreement Responses',
        'Likert Item': 'Likert Scale Item'
    },
    hover_data=['Rural areas', 'Suburban areas', 'Urban areas'], 
    height=800,
    color='Total Disagreement Count', # Optional: adds a color gradient
    color_continuous_scale='Reds'      # Optional: highlights higher disagreement
)

fig.update_layout(yaxis={'categoryorder':'total ascending'})

# --- Streamlit Display ---
st.title("Disagreement horizontal bar chart Analysis")
st.write("Most Disagreement Count (1 & 2) Across Area Types on All Category.")

# Display the plot
st.plotly_chart(fig, use_container_width=True)
# ---------------------------------------------------------
# MODULE 3: TABLE ANALYSIS
# ---------------------------------------------------------

heatmap_pivot = heatmap_pivot_z.copy()


# 1. Calculate the total disagreement count (Same logic as yours)
heatmap_pivot['Total Disagreement Count'] = heatmap_pivot[['Rural areas', 'Suburban areas', 'Urban areas']].sum(axis=1)

# 2. Reset index to make 'Likert Item' a regular column
summary_table_all_areas = heatmap_pivot.reset_index()

# --- Streamlit Display Section ---

st.header("Total Disagreement Summary")
st.write("Counts of 'Strongly Disagree' (1) and 'Disagree' (2) for each Likert Item across all Area Types:")

# Option 1: Interactive Dataframe (Allows sorting, searching, and filtering)
st.dataframe(summary_table_all_areas, use_container_width=True, hide_index=True)

# Option 2: Static Table (Use this if you want a non-interactive, print-style table)
# st.table(summary_table_all_areas)
st.markdown("""

st.plotly_chart(fig, use_container_width=True) 
# ---------------------------------------------------------
# MODULE 4: INTERPRETATION AND ANALYSIS
# ---------------------------------------------------------



### Interpretation of how respondents from all area types choose most disagreements (factors, effects, and step), to reveal the pattern of each Likert scale item count

Graphs 1 and 2 illustrate how respondents from rural, suburban, and urban areas expressed disagreement (Likert scale 1–2) toward traffic-related **factors**, **effects**, and **steps**, using a heatmap and a horizontal bar chart titled *“Disagreement Responses (1 & 2) Across Area Types”* and *“Total Disagreement Counts (1 & 2) for Each Likert Item Across All Area Types”*.

Items with higher disagreement counts indicate that respondents perceive them as **less important, less relevant, or less viable** in explaining or addressing traffic congestion. The analysis reveals that the factor **“Students Not Sharing Vehicles”** recorded the highest overall disagreement (33), with rural areas (9), suburban areas (6), and particularly urban areas (18), comprising 20 responses of *Disagree* and 13 of *Strongly Disagree*. This suggests a strong lack of belief in the practicality and importance of student vehicle sharing as a solution to traffic congestion, especially in urban contexts.

In contrast, the **“Narrow Road Factor”** recorded one of the lowest disagreement counts (5), indicating broad recognition that infrastructure limitations are a significant contributor to traffic congestion. This comparison highlights that **infrastructure-related factors are perceived as more credible and impactful than behavioural factors**.

Regarding traffic effects, the **“Unintended Road Accidents Effect”** showed a moderate level of disagreement (11), with rural (1), suburban (1), and urban areas (9), consisting of 9 *Disagree* and 2 *Strongly Disagree* responses. This suggests uncertainty—particularly in urban areas—about the direct causal relationship between congestion and road accidents, implying that congestion may contribute more to stress and near-miss situations rather than actual accidents.

For mitigation steps, the **“Vehicle Sharing Step”** recorded a notable disagreement level (14), involving rural (6), suburban (2), and urban areas (6), with 8 *Disagree* and 6 *Strongly Disagree* responses. This reflects resistance toward strategies that require behavioural or personal lifestyle changes.

In conclusion, the most disagreed items by category are:
- **Factor:** Students Not Sharing Vehicles (33)
- **Effect:** Unintended Road Accidents Effect (11)
- **Step:** Vehicle Sharing Step (14)

Overall, the findings indicate that respondents tend to **reject behaviour-based explanations and solutions**, while showing stronger agreement with **structural and infrastructural causes** of traffic congestion. All analyses presented in Graphs 1 through 6 are based on the dataset **prior to outlier handling**.
""")

