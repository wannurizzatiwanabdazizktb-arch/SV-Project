# To explore the relationship between traffic factors and congestion effect from rural perspectives.

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.header("Exploring Traffic Factors and Congestion Effects Infront School of Rural Areas")
st.write(
    """
    This dashboard explores the relationship between traffic-related factors and congestion effects in rural areas. It aims to rank traffic factors based on respondents’ perceptions and analyze how they influence congestion near schools.
    """
)

st.markdown("### 📊 Survey Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Respondents", "38",  help="Number of respondents who participated in the survey. Shows the sample size for all visualizations.", 
    border=True)
col2.metric("Study Perspective", "Rural", help="This survey captures respondents’ perceptions of traffic congestion factors and effects near rural school zones. It reflects opinions, not direct measurements or cause-effect relationships.", 
    border=True)
col3.metric("Measurement Scale", "Likert 1–5", help="Likert scale (1 = Strongly Disagree, 5 = Strongly Agree) used to rate traffic factors and congestion effects.", 
    border=True)
col4.metric("Gender Distribution", "F: 26 | M: 12", help="Number of respondents by gender. This is only for demographic context and does not affect analysis of traffic factors or effects.", 
    border=True)

          
# Load Dataset
url = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/cleaned_data%20(Izzati).csv"

# Read the dataset
df_clean = pd.read_csv(url)

#------------------------------------------------------------ 
# Bar Chart: Ranking of factor that caused trafic congestion.
#------------------------------------------------------------

# --- Title Graph ---
st.subheader("1. Bar Chart: Ranking of Factor That Caused Trafic Congestion.")

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
# Pie Chart: Percentage Distribution of Effect From The Traffic Congestion.
#--------------------------------------------------------------------------

# --- Title Graph ---
st.subheader("2. Pie Chart: Percentage Distribution of Effect From The Traffic Congestion.")

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
# Rectangular Correlation Matrix: Factors Vs Effects
#------------------------------------------------

# --- Title Graph ---
st.subheader("3. Rectangular Correlation Matrix: Traffic Factors Vs Congestion Effects")

# --- Define values ---
heatmap_cols = factors_columns + effect_columns
heatmap_corr = df_clean[heatmap_cols].corr(method="spearman")
heatmap_rect = heatmap_corr.loc[factors_columns, effect_columns]

# Round values for display
z_values = heatmap_rect.round(2).values

# --- Plotly Visualization
fig = go.Figure(
    data=go.Heatmap(
        z=z_values,
        x=heatmap_rect.columns,
        y=heatmap_rect.index,
        colorscale="sunset",
        zmin=-1, zmax=1,
        colorbar=dict(title="Spearman r"),
        text=z_values,           # numbers to display
        texttemplate="%{text}",  # show numbers inside cells
        textfont={"size":12},    # font size
    )
)

fig.update_layout(
    title="Spearman Correlation Heatmap: Factors vs Congestion Effects",
    xaxis_tickangle=-45,
    yaxis_autorange='reversed',  # highest factor on top
    width=1000,
    height=800
)

fig.data[0].hovertemplate = "Factor: %{y}<br>Effect: %{x}<br>Correlation = %{z}<extra></extra>"

# --- Show figure in Streamlit ---
st.plotly_chart(fig, use_container_width=True)

#--------------------------------------------------------- 
# Radar Chart: Percentage Score of effect from one factor.
#---------------------------------------------------------

# --- Title Graph ---
st.subheader("4. Radar Chart: Percentage Score of Effect From One Factor.")

# --- Define values ---
selected_factor = "Narrow Road Factor"
agree = df_clean[df_clean[selected_factor].isin([4,5])]
disagree = df_clean[df_clean[selected_factor].isin([1,2,3])]
disagree

agree_effect = agree[effect_columns].isin([4,5]).mean() * 100
disagree_effect = disagree[effect_columns].isin([4,5]).mean() * 100


compare_df = (
    pd.DataFrame({
        "Agree (4–5)": agree_effect,
        "Disagree (1–2)": disagree_effect
    })
    .round(1)
)

labels = compare_df.index.tolist()
labels += [labels[0]]  # close the loop

agree_values = compare_df["Agree (4–5)"].tolist()
agree_values += [agree_values[0]]

disagree_values = compare_df["Disagree (1–2)"].tolist()
disagree_values += [disagree_values[0]]

# --- Plotly Visualization ---
fig = go.Figure()

# Agree group
fig.add_trace(
    go.Scatterpolar(
        r=agree_values,
        theta=labels,
        fill='toself',
        name="Agree with Factor (4–5)",
        line=dict(color="green"),
         hovertemplate=(
            "<b>Effect:</b> %{theta}<br>"
            "<b>Agreement:</b> %{r:.1f}%"
            "<extra></extra>"
        )
    )
)

# Disagree group
fig.add_trace(
    go.Scatterpolar(
        r=disagree_values,
        theta=labels,
        fill='toself',
        name="Not Sure with Factor (1–3)",
        line=dict(color="purple"),
         hovertemplate=(
            "<b>Effect:</b> %{theta}<br>"
            "<b>Agreement:</b> %{r:.1f}%"
            "<extra></extra>"
        )
    )
)

fig.update_layout(
    title=f"Comparison of Congestion Effects by Perception of {selected_factor} (Rural)",
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    ),
    showlegend=True,
)

# --- Show figure in Streamlit ---
st.plotly_chart(fig, use_container_width=True)

#----------------------------------------------------------------
# Box Plot: Congestion Effect by Severity of a Key Traffic Factor
#----------------------------------------------------------------

# --- Title Graph ---
st.subheader("5. Stacked Bar Chart: Congestion Effect by Severity of a Key Traffic Factor.")

# --- Define Values ---
key_factor = "Narrow Road Factor"
congestion_effect = "Time Wastage Effect"

# Subset
df_subset = df_clean[[key_factor, congestion_effect]].dropna().copy()

# Recode factor into severity
df_subset["Factor Severity"] = pd.cut(
    df_subset[key_factor],
    bins=[0, 2, 3, 5],
    labels=["Low (1–2)", "Medium (3)", "High (4–5)"]
)

freq_df = df_subset.groupby(["Factor Severity", congestion_effect]).size().reset_index(name="Frequency")

# --- Plotly Visualization ---
fig = px.bar(
    freq_df,
    x="Factor Severity",
    y="Frequency",
    color=congestion_effect,
    barmode="group",
     color_discrete_sequence=["purple", "mediumpurple", "gold", "lightgreen", "green"],
    title=f"Distribution of {congestion_effect} by Severity of {key_factor} (Rural Areas)",
    labels={
        "Factor Severity": "Severity of Traffic Factor",
        "Frequency": "Number of Respondents",
        congestion_effect: "Congestion Effect (Likert Scale)"
    }
)

# --- Show figure in Streamlit ---
st.plotly_chart(fig, use_container_width=True)
