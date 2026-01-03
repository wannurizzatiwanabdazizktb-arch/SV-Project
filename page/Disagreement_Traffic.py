import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Disagreement Traffic Congestion Survey",
    page_icon="📊",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("📊 Traffic Congestion Survey")
    st.markdown("---")
    st.info("Use the menu to explore different analysis modules.")
    st.caption("👩🏻‍💻 Created by Nurul Ain Maisarah Hamidin (2025)")

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_data.csv")

merged_df = load_data()

# ---------------------------------------------------------
# DEFINE LIKERT COLUMNS (EDIT TO MATCH CSV)
# ---------------------------------------------------------
likert_cols = merged_df.columns[3:10]  # adjust if needed

# Example grouping
factor_cols = likert_cols[:3]
effect_cols = likert_cols[3:5]
step_cols = likert_cols[5:]

all_likert_cols = factor_cols.tolist() + effect_cols.tolist() + step_cols.tolist()

# ---------------------------------------------------------
# DISAGREEMENT COUNT
# ---------------------------------------------------------
result = {}

for col in likert_cols:
    result[col] = (
        merged_df[merged_df[col].isin([1, 2])]
        .groupby("Area Type")[col]
        .count()
    )

disagree_df = pd.DataFrame(result).fillna(0).astype(int)

st.subheader("Count of Strongly Disagree (1) & Disagree (2)")
st.dataframe(disagree_df, use_container_width=True)

# ---------------------------------------------------------
# HEATMAP
# ---------------------------------------------------------
heatmap_data = []

for area in merged_df["Area Type"].unique():
    for col in all_likert_cols:
        area_data = merged_df[merged_df["Area Type"] == area]
        sd = (area_data[col] == 1).sum()
        d = (area_data[col] == 2).sum()

        heatmap_data.append({
            "Area Type": area,
            "Likert Item": col,
            "Total": sd + d,
            "SD": sd,
            "D": d
        })

heatmap_df = pd.DataFrame(heatmap_data)

pivot = heatmap_df.pivot(
    index="Likert Item",
    columns="Area Type",
    values="Total"
).fillna(0)

fig = go.Figure(go.Heatmap(
    z=pivot.values,
    x=pivot.columns,
    y=pivot.index,
    colorscale="YlGnBu",
    text=pivot.values,
    texttemplate="%{text}"
))

fig.update_layout(height=800)
st.plotly_chart(fig, use_container_width=True)

# --- Data Preparation ---
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

# Sort for better visualization
disagreement_summary_df_sorted = disagreement_summary_df.sort_values(
    'Total Disagreement Count', ascending=True
)

# --- Create Plotly Figure ---
fig = px.bar(
    disagreement_summary_df_sorted,
    x='Total Disagreement Count',
    y='Likert Item',
    orientation='h',
    title='Total Disagreement Counts (1 & 2) Across All Area Types',
    labels={
        'Total Disagreement Count': 'Total Disagreement Responses',
        'Likert Item': 'Survey Item'
    },
    hover_data=['Rural areas', 'Suburban areas', 'Urban areas', 'Total Disagreement Count'],
    height=800,
    color='Total Disagreement Count', # Optional: adds a color gradient to the bars
    color_continuous_scale='Viridis'   # Optional: visual clarity
)

# Clean up layout
fig.update_layout(
    yaxis={'categoryorder':'total ascending'},
    margin=dict(l=200), # Ensure long labels have room
    template='plotly_white'
)

# --- Display in Streamlit ---
st.plotly_chart(fig, use_container_width=True)

# Optional: Add a raw data expander below the chart
with st.expander("View Raw Data Table"):
    st.dataframe(disagreement_summary_df_sorted.sort_values('Total Disagreement Count', ascending=False))

import pandas as pd
import streamlit as st

# --- Data Processing ---
# Calculate the total disagreement count for each Likert Item across all areas
heatmap_pivot['Total Disagreement Count'] = heatmap_pivot[['Rural areas', 'Suburban areas', 'Urban areas']].sum(axis=1)

# Reset index to make 'Likert Item' a regular column
summary_table_all_areas = heatmap_pivot.reset_index()

# Sort by total count descending so the most significant items appear at the top
summary_table_all_areas = summary_table_all_areas.sort_values(by='Total Disagreement Count', ascending=False)

# --- Streamlit Display ---
st.subheader("Total Disagreement Counts (1 & 2) Across All Area Types")

# Use st.dataframe for an interactive table
st.dataframe(
    summary_table_all_areas, 
    use_container_width=True, 
    hide_index=True
)

# Optional: Add a brief metric summary to highlight the most disagreed-upon item
top_item = summary_table_all_areas.iloc[0]['Likert Item']
top_val = summary_table_all_areas.iloc[0]['Total Disagreement Count']

st.info(f"**Highest Disagreement:** {top_item} with {int(top_val)} total responses.") 

import pandas as pd
import plotly.express as px
import streamlit as st

# --- Streamlit Page Config ---
st.set_page_config(page_title="Survey Disagreement Analysis", layout="wide")

# --- Title ---
st.title("How respondents from area type choose disagreement")
st.subheader("Revealing gaps between real-world experiences and survey assumptions")

# --- Data Processing ---
# (Assuming likert_cols and merged_df are already defined in your environment)
factor_cols = [col for col in likert_cols if 'Factor' in col]
effect_cols = [col for col in likert_cols if 'Effect' in col]
step_cols = [col for col in likert_cols if 'Step' in col]

all_disagreement_data = []

for area in ['Rural areas', 'Suburban areas', 'Urban areas']:
    for col in likert_cols:
        count = merged_df.loc[merged_df['Area Type'] == area, col].isin([1, 2]).sum()
        if count > 0:
            if col in factor_cols:
                category = 'Factor'
            elif col in effect_cols:
                category = 'Effect'
            else:
                category = 'Step'
            
            all_disagreement_data.append({
                'Area Type': area,
                'Likert Item': col,
                'Category': category,
                'Disagreement Count': count
            })

stacked_df = pd.DataFrame(all_disagreement_data)

# --- Streamlit Sidebar Filter ---
st.sidebar.header("Filter Options")
selected_categories = st.sidebar.multiselect(
    "Select Categories to Display:",
    options=stacked_df['Category'].unique(),
    default=stacked_df['Category'].unique()
)

# Filter the dataframe based on selection
filtered_df = stacked_df[stacked_df['Category'].isin(selected_categories)]

# --- Create Stacked Bar Chart ---
# Using the filtered dataframe
fig = px.bar(
    filtered_df, 
    x='Area Type',
    y='Disagreement Count',
    color='Category',
    title='Stacked Disagreement Responses by Category and Area Type',
    labels={
        'Disagreement Count': 'Number of Disagreement Responses',
        'Area Type': 'Area Type',
        'Category': 'Item Category'
    },
    # Keep your custom color mapping
    color_discrete_map={'Factor':'#1f77b4','Effect':'#ff7f0e','Step':'#2ca02c'},
    hover_data={'Likert Item': True, 'Category': False, 'Disagreement Count': True}
)

fig.update_layout(
    barmode='stack',
    xaxis_title='Area Type',
    yaxis_title='Number of Disagreement Responses',
    template='plotly_white',
    height=600,
    legend_title_text='Item Category',
    xaxis={'categoryorder':'total descending'} # Sorts areas by total disagreement volume
)

# --- Display in Streamlit ---
st.plotly_chart(fig, use_container_width=True)

# Analysis Note
with st.expander("Interpret the Pattern"):
    st.write("""
    **Insight:** If 'Urban areas' show significantly higher disagreement counts in the 'Step' category, 
    it may suggest that proposed solutions (Steps) do not align with the practical infrastructure 
    limitations found in dense urban environments.
    """)

import pandas as pd
import streamlit as st

# --- Title ---
st.title("Survey Analysis: Disagreement Breakdown")
st.markdown("Detailed list of Likert items, categories, and disagreement counts categorized by area type.")

# --- Data Processing ---
# Sort the dataframe as requested: Category first, then Item, then Area Type
sorted_disagreement_df = combined_disagreement_df.sort_values(
    by=['Category', 'Likert Item', 'Area Type']
)

# --- Streamlit Display ---
st.subheader("Likert Items and Disagreement Counts")

# Display the interactive dataframe
st.dataframe(
    sorted_disagreement_df, 
    use_container_width=True, 
    hide_index=True
)

# --- Optional: Download Button ---
# This allows users to export the sorted table to CSV directly from the Streamlit app
csv = sorted_disagreement_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Table as CSV",
    data=csv,
    file_name='disagreement_counts_summary.csv',
    mime='text/csv',
)


import pandas as pd
import plotly.express as px
import streamlit as st

# --- Streamlit Title ---
st.title("Rural Respondent Rejection Analysis")
st.markdown("### How majority most clearly reject: Comparison of Strongly Disagree (1) and Disagree (2)")

# --- Data Processing ---
# (Assumes merged_df, likert_cols, factor_cols, effect_cols, step_cols are defined)

# Filter data for Rural respondents
rural_df = merged_df[merged_df['Area Type'] == 'Rural areas']

disagreement_data = []

for col in likert_cols:
    if col in rural_df.columns:
        count_sd = (rural_df[col] == 1).sum()
        count_d  = (rural_df[col] == 2).sum()
        
        # Determine category
        category = 'Factor' if col in factor_cols else 'Effect' if col in effect_cols else 'Step'
        
        if count_sd > 0:
            disagreement_data.append({
                'Likert Item': col,
                'Category': category,
                'Disagreement Count': count_sd,
                'Disagreement Type': 'Strongly Disagree (1)'
            })
        if count_d > 0:
            disagreement_data.append({
                'Likert Item': col,
                'Category': category,
                'Disagreement Count': count_d,
                'Disagreement Type': 'Disagree (2)'
            })

disagreement_df_rural = pd.DataFrame(disagreement_data)

# --- Streamlit Sidebar Filters ---
st.sidebar.header("Chart Filters")
selected_cats = st.sidebar.multiselect(
    "Select Category:",
    options=disagreement_df_rural['Category'].unique(),
    default=disagreement_df_rural['Category'].unique()
)

# Filter the data
filtered_rural_df = disagreement_df_rural[disagreement_df_rural['Category'].isin(selected_cats)]

# Define Item Order for Y-axis
item_order = (
    filtered_rural_df.sort_values(['Category', 'Disagreement Count'])['Likert Item']
    .unique()
    .tolist()
)
filtered_rural_df['Likert Item'] = pd.Categorical(filtered_rural_df['Likert Item'], categories=item_order, ordered=True)

# --- Create Plotly Bubble Chart ---
fig = px.scatter(
    filtered_rural_df,
    x='Disagreement Count',
    y='Likert Item',
    size='Disagreement Count',
    color='Disagreement Type',
    color_discrete_map={'Strongly Disagree (1)':'#1f77b4','Disagree (2)':'#28a745'},
    title='Disagreement Responses (1 vs 2) among Rural Respondents',
    labels={
        'Disagreement Count': 'Number of Responses',
        'Likert Item': 'Likert Scale Item',
        'Disagreement Type': 'Level'
    },
    hover_data=['Category', 'Disagreement Count'],
    size_max=25
)

fig.update_layout(
    xaxis_title='Number of Responses',
    yaxis_title='Likert Scale Item',
    template='plotly_white',
    height=800,
    margin=dict(l=200) # Prevents long text from being cut off
)

# --- Display in Streamlit ---

st.plotly_chart(fig, use_container_width=True)

# Highlight Key Metric
if not filtered_rural_df.empty:
    max_reject = filtered_rural_df.loc[filtered_rural_df['Disagreement Count'].idxmax()]
    st.info(f"**Highest Rejection Point:** Rural respondents most strongly rejected: **{max_reject['Likert Item']}**.")

import pandas as pd
import streamlit as st

# --- Streamlit Header ---
st.title("Rural Respondent Disagreement Summary")
st.markdown("Detailed breakdown of 'Strongly Disagree' and 'Disagree' counts specifically for rural areas.")

# --- Data Processing ---
# (Assuming rural_df and likert_cols are already defined)

disagreement_data_rural = []
for col in likert_cols:
    if col in rural_df.columns:
        count_sd = (rural_df[col] == 1).sum()
        count_d  = (rural_df[col] == 2).sum()

        if count_sd > 0 or count_d > 0:
            disagreement_data_rural.append({
                'Likert Item': col,
                'Strongly Disagree (1)': count_sd,
                'Disagree (2)': count_d
            })

disagreement_df_rural = pd.DataFrame(disagreement_data_rural)

# Group by Likert Item and calculate a Total for sorting
rural_disagreement_summary = disagreement_df_rural.groupby('Likert Item')[[ 
    'Strongly Disagree (1)', 'Disagree (2)'
]].sum().reset_index()

# Add a total column to help identify the "majority rejection" items
rural_disagreement_summary['Total Disagreement'] = (
    rural_disagreement_summary['Strongly Disagree (1)'] + 
    rural_disagreement_summary['Disagree (2)']
)

# Sort by Total Disagreement descending
rural_disagreement_summary = rural_disagreement_summary.sort_values(
    by='Total Disagreement', ascending=False
)

# --- Streamlit Display ---
st.subheader("Summary Table: Rural Respondents")

# Use st.dataframe for an interactive, searchable table
st.dataframe(
    rural_disagreement_summary, 
    use_container_width=True, 
    hide_index=True
)

# --- Insight Sidebar (Optional) ---
st.sidebar.header("Rural Insights")
if not rural_disagreement_summary.empty:
    top_rejected = rural_disagreement_summary.iloc[0]['Likert Item']
    st.sidebar.info(f"The item with the most rural disagreement is: **{top_rejected}**")   

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Urban Disagreement Analysis", layout="wide")

# --- Title ---
st.title("How majority most clearly reject from urban respondent rate")
st.markdown("### Comparison of Strongly Disagree (1) and Disagree (2)")

# --- Data Processing ---
# (Assumes merged_df and likert_cols are already defined)
urban_df = merged_df[merged_df['Area Type'] == 'Urban areas']

def classify_item(col):
    if 'Factor' in col:
        return 'Factor'
    elif 'Effect' in col:
        return 'Effect'
    elif 'Step' in col:
        return 'Step'
    else:
        return 'Other'

disagreement_data = []

for col in likert_cols:
    if col in urban_df.columns:
        count_sd = (urban_df[col] == 1).sum()
        count_d  = (urban_df[col] == 2).sum()

        if count_sd > 0 or count_d > 0:
            disagreement_data.append({
                'Likert Scale Item': col,
                'Item Category': classify_item(col),
                'Strongly Disagree (1)': count_sd,
                'Disagree (2)': count_d
            })

disagreement_df = pd.DataFrame(disagreement_data)
disagreement_df['Total'] = disagreement_df['Strongly Disagree (1)'] + disagreement_df['Disagree (2)']

# --- Streamlit Sidebar Filters ---
st.sidebar.header("Filter Controls")
selected_cats = st.sidebar.multiselect(
    "Select Item Categories:",
    options=disagreement_df['Item Category'].unique(),
    default=disagreement_df['Item Category'].unique()
)

# Apply Filter
filtered_df = disagreement_df[disagreement_df['Item Category'].isin(selected_cats)]
filtered_df = filtered_df.sort_values('Total', ascending=True)

# --- Create Plotly Figure ---
fig = go.Figure()

# Strongly Disagree Trace
fig.add_trace(
    go.Bar(
        x=filtered_df['Strongly Disagree (1)'],
        y=filtered_df['Likert Scale Item'],
        orientation='h',
        name='Strongly Disagree (1)',
        marker=dict(color='#1f77b4'),
        customdata=filtered_df[['Item Category', 'Strongly Disagree (1)']],
        hovertemplate='<b>%{y}</b><br>Category: %{customdata[0]}<br>Count: %{customdata[1]}<extra></extra>'
    )
)

# Disagree Trace
fig.add_trace(
    go.Bar(
        x=filtered_df['Disagree (2)'],
        y=filtered_df['Likert Scale Item'],
        orientation='h',
        name='Disagree (2)',
        marker=dict(color='#2ca02c'),
        customdata=filtered_df[['Item Category', 'Disagree (2)']],
        hovertemplate='<b>%{y}</b><br>Category: %{customdata[0]}<br>Count: %{customdata[1]}<extra></extra>'
    )
)

fig.update_layout(
    title='Disagreement Responses (1 vs 2) among Urban Respondents',
    xaxis_title='Number of Disagreement Responses',
    yaxis_title='Likert Scale Item',
    legend_title_text='Disagreement Level',
    barmode='group',
    template='plotly_white',
    height=800,
    margin=dict(l=250) # Extra room for long urban factor names
)

# --- Display in Streamlit ---

st.plotly_chart(fig, use_container_width=True)

# --- Summary Table Expander ---
with st.expander("View Detailed Urban Data Table"):
    st.dataframe(filtered_df.sort_values('Total', ascending=False), use_container_width=True, hide_index=True) 

import pandas as pd
import streamlit as st

# --- Streamlit Title ---
st.title("Urban Respondent Disagreement Summary")
st.markdown("Analysis of 'Strongly Disagree' and 'Disagree' responses within Urban Area Types.")

# --- Data Processing ---
# (Assumes urban_df and likert_cols are already defined in your script)

disagreement_data_urban = []
for col in likert_cols:
    if col in urban_df.columns:
        count_sd = (urban_df[col] == 1).sum()
        count_d  = (urban_df[col] == 2).sum()

        if count_sd > 0 or count_d > 0:
            disagreement_data_urban.append({
                'Likert Item': col,
                'Strongly Disagree (1)': count_sd,
                'Disagree (2)': count_d
            })

disagreement_df_urban = pd.DataFrame(disagreement_data_urban)

# Group and aggregate
urban_disagreement_summary = disagreement_df_urban.groupby('Likert Item')[[
    'Strongly Disagree (1)', 'Disagree (2)'
]].sum().reset_index()

# Add a total column for better sorting and pattern recognition
urban_disagreement_summary['Total Rejections'] = (
    urban_disagreement_summary['Strongly Disagree (1)'] + 
    urban_disagreement_summary['Disagree (2)']
)

# Sort by most rejected items first
urban_disagreement_summary = urban_disagreement_summary.sort_values(by='Total Rejections', ascending=False)

# --- Streamlit Display ---
st.subheader("Summary Table: Urban Respondents")

# st.dataframe provides an interactive, searchable table
st.dataframe(
    urban_disagreement_summary, 
    use_container_width=True, 
    hide_index=True
)

# --- Summary Metric ---
if not urban_disagreement_summary.empty:
    top_item = urban_disagreement_summary.iloc[0]['Likert Item']
    top_val = urban_disagreement_summary.iloc[0]['Total Rejections']
    st.info(f"**Insight:** The item most rejected by urban respondents is **'{top_item}'** with {int(top_val)} total disagreements.")

import pandas as pd
import plotly.express as px
import streamlit as st

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Suburban Analysis", layout="wide")

# --- Title ---
st.title("How majority most clearly reject from Suburban respondent rate")
st.markdown("### Comparison of Strongly Disagree (1) and Disagree (2)")

# --- Data Processing ---
# (Assumes merged_df, likert_cols, factor_cols, effect_cols, step_cols are defined)
suburban_df = merged_df[merged_df['Area Type'] == 'Suburban areas']

disagreement_data = []
for col in likert_cols:
    count_sd = (suburban_df[col] == 1).sum()
    count_d  = (suburban_df[col] == 2).sum()
    
    if count_sd > 0 or count_d > 0:
        # Determine category
        category = 'Factor' if col in factor_cols else 'Effect' if col in effect_cols else 'Step' if col in step_cols else 'Other'

        disagreement_data.append({
            'Likert Item': col,
            'Category': category,
            'Strongly Disagree (1)': count_sd,
            'Disagree (2)': count_d
        })

disagreement_df = pd.DataFrame(disagreement_data)

# --- Sidebar Filters ---
st.sidebar.header("Filter Visualization")
selected_categories = st.sidebar.multiselect(
    "Select Categories:",
    options=disagreement_df['Category'].unique(),
    default=disagreement_df['Category'].unique()
)

# Filter the dataframe
filtered_df = disagreement_df[disagreement_df['Category'].isin(selected_categories)]

# Melt data for radar chart
disagreement_melted = filtered_df.melt(
    id_vars=['Likert Item','Category'],
    value_vars=['Strongly Disagree (1)','Disagree (2)'],
    var_name='Disagreement Type',
    value_name='Count'
)

# --- Create Radar Chart ---
if not disagreement_melted.empty:
    fig = px.line_polar(
        disagreement_melted,
        r='Count',
        theta='Likert Item',
        color='Disagreement Type',
        line_close=True,
        markers=True,
        color_discrete_map={'Strongly Disagree (1)':'#1f77b4','Disagree (2)':'#28a745'},
        title='Disagreement Responses (1 vs 2) among Suburban Respondents'
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(title='Responses', visible=True, tickfont_size=10),
            angularaxis=dict(tickfont_size=10)
        ),
        legend_title_text='Disagreement Level',
        template='plotly_white',
        height=800
    )

    # --- Display in Streamlit ---
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected categories.")

# --- Data Summary Table ---
with st.expander("View Detailed Suburban Disagreement Table"):
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)   

import pandas as pd
import streamlit as st

# --- Streamlit Header ---
st.title("Suburban Respondent Disagreement Summary")
st.markdown("Detailed breakdown of 'Strongly Disagree' and 'Disagree' counts for Suburban areas.")

# --- Data Processing ---
# (Assumes suburban_df and likert_cols are already defined)

disagreement_data_suburban = []
for col in likert_cols:
    # Skip 'Students Not Sharing Vehicles'
    if col == 'Students Not Sharing Vehicles':
        continue

    if col in suburban_df.columns:
        count_sd = (suburban_df[col] == 1).sum()
        count_d  = (suburban_df[col] == 2).sum()

        if count_sd > 0 or count_d > 0:
            disagreement_data_suburban.append({
                'Likert Item': col,
                'Strongly Disagree (1)': count_sd,
                'Disagree (2)': count_d
            })

disagreement_df_suburban = pd.DataFrame(disagreement_data_suburban)

# Group and aggregate
suburban_disagreement_summary = disagreement_df_suburban.groupby('Likert Item')[[ 
    'Strongly Disagree (1)', 'Disagree (2)'
]].sum().reset_index()

# Add a total column for better pattern analysis
suburban_disagreement_summary['Total Rejections'] = (
    suburban_disagreement_summary['Strongly Disagree (1)'] + 
    suburban_disagreement_summary['Disagree (2)']
)

# Sort by most rejected items first
suburban_disagreement_summary = suburban_disagreement_summary.sort_values(
    by='Total Rejections', ascending=False
)

# --- Streamlit Display ---
st.subheader("Summary Table: Suburban Respondents")

# Use st.dataframe for an interactive, searchable table
st.dataframe(
    suburban_disagreement_summary, 
    use_container_width=True, 
    hide_index=True
)

# --- Insights Alert ---
if not suburban_disagreement_summary.empty:
    top_item = suburban_disagreement_summary.iloc[0]['Likert Item']
    st.info(f"**Key Finding:** Suburban respondents showed the highest level of disagreement on: **{top_item}**.")
