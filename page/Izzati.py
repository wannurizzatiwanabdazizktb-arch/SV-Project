# To explore the relationship between traffic factors and congestion effect from rural perspectives.

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.header("Exploring Traffic Factors and Congestion Effects infront School of Rural Areas")
st.write(
    """
    This dashboard explores the relationship between traffic-related factors and congestion effects in rural areas.
    """
)
          
# Load Dataset
url = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/cleaned_data%20(Izzati).csv"

# Read the dataset
df_clean = pd.read_csv(url)

#------------------------------------------------------------ 
# Bar Chart: Ranking of factor that caused trafic congestion.
#------------------------------------------------------------

# --- Title Graph ---
st.subheader("1. Bar Chart: Ranking of factor that caused trafic congestion.")

# --- Grouping columns ---
factors_columns = [
    "Lack of Parking Space Factor",
    "Rainy Weather Factor",
    "Single Gate Factor",
    "Leaving Work Late Factor",
    "Increasing Population Factor",
    "Students Not Sharing Vehicles",
    "Lack of Pedestrian Bridge Factor",
    "Damaged Road Factor",
    "Construction/Roadworks Factor",
    "Late Drop-off/Pick-up Factor",
    "Narrow Road Factor",
    "Undisciplined Driver Factor"
]

# --- Calculate % agree ---
ranking_df = (
    df_clean[factors_columns]
    .apply(lambda x: x.isin([4,5]).mean() * 100)
    .sort_values(ascending=False)
    .reset_index()
)
ranking_df.columns = ["Traffic Factor", "Percent Agree"]
ranking_df["Percent Agree"] = ranking_df["Percent Agree"].round(1)

# --- Plotly bar chart ---
custom_colors = [[0, "green"], [0.5, "yellow"], [1, "purple"]]

fig = px.bar(
    ranking_df,
    x="Percent Agree",
    y="Traffic Factor",
    orientation='h',
    text="Percent Agree",
    color="Percent Agree",
    color_continuous_scale=custom_colors,
    title="Ranking of Traffic Congestion Factors (Rural Areas)",
    labels={"Percent Agree":"% of Respondents Agreeing (4–5)", "Traffic Factor":"Traffic Factor"}
)
fig.update_layout(yaxis={'categoryorder':'total ascending'})
fig.update_traces(texttemplate="%{text}%", textposition='inside')

# --- Streamlit Display ---
st.plotly_chart(fig, use_container_width=True)

#--------------------------------------------------------------------------
# Pie Chart: Percentage distribution of effect from the traffic congestion.
#--------------------------------------------------------------------------

# --- Title Graph ---
st.subheader("2. Pie Chart: Percentage distribution of effect from the traffic congestion.")

# --- Grouping columns ---
effect_columns = [
    "Unintended Road Accidents Effect",
    "Time Wastage Effect",
    "Pressure on Road Users Effect",
    "Students Late to School Effect",
    "Environmental Pollution Effect",
    "Fuel Wastage Effect",
]

# --- Calculate Percentage ---
# Count values and convert to percentages
pie_df = (
    df_clean[effect_columns]
    .apply(lambda x: x.isin([4,5]).mean() * 100)
    .sort_values(ascending=False)
    .reset_index()
)
pie_df.columns = ["Effect Congestion", "Percentage"]
pie_df["Percentage"] = pd.to_numeric(pie_df["Percentage"], errors='coerce')  # convert to numeric
pie_df["Percentage"] = pie_df["Percentage"].round(1)  # round to 1 decimal place

# --- Plotly Visualization ---
fig = px.pie(
    pie_df,
    names = 'Effect Congestion',
    values = "Percentage",
    title=f"Distribution of {'Effect Congestion'} (Rural Areas)",
    color_discrete_sequence=["purple", "yellow", "green", "lime", "brown", "orange"]  # You can change color theme
)

# Optional: show % inside pie slices
fig.update_traces(textinfo='percent', hoverinfo='label+percent')
fig.update_layout(legend=dict(orientation="h", y=-0.1))

# --- Show figure in Streamlit ---
st.plotly_chart(fig, use_container_width=True)

#------------------------------------------------
# Heatmap: Traffic Factors vs Congestion Effects.
#------------------------------------------------

#--------------------------------------------------------- 
# Radar Chart: Percentage score of effect from one factor.
#---------------------------------------------------------

#----------------------------------------------------------------
# Box Plot: Congestion Effect by Severity of a Key Traffic Factor
#----------------------------------------------------------------
