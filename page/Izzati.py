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

# ---  Interpretation ---
st.markdown(
    """
    <div style="text-align: justify;">
    Rural traffic congestion infornt of school is perceived to be driven mainly by infrastructure challenges, with narrow roads and construction works identified as the most critical causes nearly 90% agreement, followed closely by damaged roads and population growth. Secondary concerns such as limited parking, rainy weather, and undisciplined drivers also contribute significantly. While practical issues like single gate access and late commuting habits are seen as moderately impactful. At the lowest level, fewer than half of respondents view students not sharing vehicles as a factor that contribute to trafic congestion infront of school. Overall, the visualization underscores that physical road conditions and infrastructure limitations are the dominant drivers of congestion in rural areas school, while behavioral and scheduling factors play supporting roles.
    </div>
    """,
    unsafe_allow_html=True
)

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

# ---  Interpretation ---
st.markdown(
    """
    <div style="text-align: justify;">
    The distribution of congestion effects in rural areas reveals that the impact is spread quite equally across multiple areas with minor differences that highlight priorities. Time wastage emerges as the most significant effect which highlights how traffic reduces daily efficiency and production. Closely aligned are pressure on road users and students arriving late to school, which point to both psychological stress and educational disruption as critical social effects. Fuel waste has led to economic effects, and unintentional traffic accidents draw attention to safety concerns that worsen the issue. Although environmental pollution ranks lowest, its presence signals long-term sustainability concerns that cannot be ignored. The visualization suggests that congestion in rural areas is not dominated by a single effect but rather creates a multi-layered impact. Effective treatments must be comprehensive that address both current road user suffering and ongoing root causes according to this balanced distribution.
    </div>
    """,
    unsafe_allow_html=True
)

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

# ---  Interpretation ---
st.markdown(
    """
    <div style="text-align: justify;">
    This Spearman correlation heatmap provides a detailed understanding of how specific congestion factors relate to various effects in rural areas which reveal the pattern of these relationship. Notably, undisciplined drivers show a strong positive correlation with unintended road accidents which suggest that behavioral issues significantly compromise road safety. Similarly, narrow roads and construction/roadworks are strongly linked to time wastage and pressure on road users which support that infrastructure limitations play a critical part in stress and inefficiency of road users due to congestion. Besides that, students arriving late to school are most correlated with late work and late drop-off/pick-up which indicate the impact of schedule patterns on academic punctuality. In the meantime, factors like rainy weather, single gate access, and damaged roads are somewhat linked to fuel waste and environmental pollution. This suggests that environmental and physical conditions lead to financial inefficiency and environmental problems. Overall, the heatmap emphasizes that various congestion impacts result from separate but related causes. In order for focused actions to be successful, they must be in line with these particular factor-effect correlations. 
    </div>
    """,
    unsafe_allow_html=True
)

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

# ---  Interpretation ---
st.markdown(
    """
    <div style="text-align: justify;">
    This radar chart offers insight into how perceptions of traffic congestion effects align with respondents’ views on narrow roads as a contributing factor in rural areas. Respondents who strongly agree that narrow roads contribute to congestion consistently report higher perceived severity across all measured congestion effects which suggest a group of serious concerns rather than individual opinions. The strongest correlation shows in time wastage and pressure on road users, demonstrating that those who consider narrow roads as problematic are particularly vulnerable to congestion-related delays and psychological stress. Significantly, increased agreement is also seen for effects like unintended road accidents, fuel waste, and environmental pollution which reflect a wider belief that problems associated with traffic congestion go beyond merely irritation. On the other hand, those who are unsure or less aware about the effect of narrow roadways have more common and moderate views. This suggest less differentiation in the view of the effects of congestion. The radar chart emphasizes how infrastructural perceptions affect broader views on traffic conditions in rural school environments by showing a pattern of perception agreement where opinion in a particular congestion factor corresponds with a more thorough recognition of congestion-related problems.
    </div>
    """,
    unsafe_allow_html=True
)

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

# ---  Interpretation ---
st.markdown(
    """
    <div style="text-align: justify;">
    This data shows that narrow roads are a major cause of traffic delays in rural areas. Most people surveyed feel this is a "High" severity problem, and they report that it leads to the maximum amount of time wasted. Interestingly, nobody rated this as a "Low" problem, meaning narrow roads are almost always seen as a significant issue. In short, the narrower and more difficult the road is, the more time people lose which suggest that road improvements as the most effective way to reduce travel delays in rural regions.
    """,
    unsafe_allow_html=True
)
