import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")

# ================= DATA LOADING =================
@st.cache_data
def load_data():
    df = pd.read_csv("traffic_survey.csv")
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
    return df

df = load_data()

effect_cols = [
    "Unintended Road Accidents Effect",
    "Time Wastage Effect",
    "Pressure on Road Users Effect",
    "Students Late to School Effect",
    "Environmental Pollution Effect",
    "Fuel Wastage Effect",
]

cause_cols = [
    "Undisciplined Driver Factor",
    "Narrow Road Factor",
    "Single Gate Factor",
    "Lack of Parking Space Factor",
]

# ================= TITLE =================
st.title("🚦 Interactive Analysis of Traffic Congestion Around Schools")

st.markdown("""
This interactive dashboard explores how traffic congestion around schools affects safety,
time efficiency, stress, punctuality, environment, and fuel usage.
Use the filters to explore different perspectives.
""")

# ================= SUMMARY METRICS =================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Respondents", len(df))

with c2:
    st.metric("Most Common Area Type", df["Area Type"].mode()[0])

with c3:
    st.metric("Likert Scale", "1 – 5")

with c4:
    gender_counts = df["Gender"].value_counts()
    st.metric("Gender Split", f"F: {gender_counts.get('Female',0)} | M: {gender_counts.get('Male',0)}")

st.divider()

# ================= FILTERS =================
st.subheader("🔍 Filters")

f1, f2, f3 = st.columns(3)

with f1:
    gender = st.selectbox("Gender", ["All"] + sorted(df["Gender"].dropna().unique()))

with f2:
    status = st.selectbox("Status", ["All"] + sorted(df["Status"].dropna().unique()))

with f3:
    area = st.selectbox("Area Type", ["All"] + sorted(df["Area Type"].dropna().unique()))

chosen_effect = st.selectbox("Focus Effect", effect_cols)

# Apply filters
sub = df.copy()
if gender != "All":
    sub = sub[sub["Gender"] == gender]
if status != "All":
    sub = sub[sub["Status"] == status]
if area != "All":
    sub = sub[sub["Area Type"] == area]

st.info(f"Responses after filtering: {len(sub)}")

if sub.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# ================= 1. EFFECT RANKING =================
st.subheader("1️⃣ Ranking of Congestion Effects")

mean_effects = sub[effect_cols].mean().sort_values()

fig1 = px.bar(
    mean_effects,
    x=mean_effects.values,
    y=mean_effects.index,
    orientation="h",
    labels={"x": "Mean Likert Score", "y": ""},
    color=mean_effects.values,
    color_continuous_scale="Magma",
)

fig1.update_layout(height=350)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("""  
The ranking of congestion effects is based on the mean Likert score (1–5) for each effect.
Effects with higher mean scores indicate stronger agreement among respondents that the issue
is a significant consequence of traffic congestion around school areas.

The results show that effects such as *Time Wastage*, *Students Late to School*, and
*Environmental Pollution* are perceived as more serious compared to other effects.
This suggests that congestion primarily impacts daily efficiency, punctuality, and
environmental quality, making these areas critical for intervention.
""")

# ================= 2. BOX PLOTS =================
st.subheader(f"2️⃣ Distribution of {chosen_effect}")

c1, c2 = st.columns(2)

with c1:
    if sub["Gender"].nunique() > 1:
        fig2 = px.box(
            sub,
            x="Gender",
            y=chosen_effect,
            points="all",
            title="By Gender"
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Only one gender available.")

with c2:
    if sub["Status"].nunique() > 1:
        fig3 = px.box(
            sub,
            x="Status",
            y=chosen_effect,
            points="all",
            title="By Status"
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Only one status available.")

st.markdown("""  
The box plots illustrate the distribution of responses for the selected effect across
different genders and respondent statuses. Differences in median values indicate variation
in perception between groups.

A higher median score suggests stronger agreement that the selected effect is caused by
traffic congestion. Wider interquartile ranges reflect greater variability in opinions,
while narrower ranges indicate more consistent perceptions within a group.
These differences highlight how demographic characteristics influence congestion-related
experiences.
""")

# ================= 3. GROUPED BAR =================
st.subheader("3️⃣ Key Effects by Status")

key_effects = [
    "Time Wastage Effect",
    "Students Late to School Effect",
    "Unintended Road Accidents Effect",
]

status_means = sub.groupby("Status")[key_effects].mean().reset_index()

fig4 = px.bar(
    status_means,
    x="Status",
    y=key_effects,
    barmode="group",
    labels={"value": "Mean Score", "variable": "Effect"},
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("""  
This grouped bar chart compares mean scores of key congestion effects across different
respondent statuses. Higher mean scores for a particular status group indicate that the
group perceives the effect more strongly.

For instance, if students or parents report higher mean scores for *Time Wastage* and
*Students Late to School*, it suggests that these groups are more directly affected by
school-area congestion. This insight is useful for identifying which stakeholders are most
impacted.
""")

# ================= 4. HEATMAP =================
st.subheader("4️⃣ Cause–Effect Correlation Heatmap")

corr = sub[cause_cols + effect_cols].corr().loc[cause_cols, effect_cols]

fig5 = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="Blues",
    aspect="auto"
)

fig5.update_layout(height=400)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("""  
The heatmap displays the correlation between congestion causes and their perceived effects.
Darker shades indicate stronger positive relationships.

Strong correlations suggest that when respondents strongly agree that a particular cause
(e.g., lack of parking space or narrow roads) exists, they also strongly agree that related
effects (such as time wastage or fuel wastage) occur. These relationships help identify
key root causes contributing to congestion-related problems.
""")

# ================= 5. STACKED BAR =================
st.subheader(f"5️⃣ Likert Distribution of {chosen_effect} by Gender")

if sub["Gender"].nunique() > 1:
    dist = (
        sub.groupby("Gender")[chosen_effect]
        .value_counts(normalize=True)
        .rename("proportion")
        .reset_index()
    )

    fig6 = px.bar(
        dist,
        x="Gender",
        y="proportion",
        color=chosen_effect,
        barmode="stack",
        labels={"proportion": "Proportion"},
    )

    st.plotly_chart(fig6, use_container_width=True)
else:
    st.info("Only one gender available.")

st.markdown("""  
The stacked bar chart shows the proportion of responses across the Likert scale for each
gender. A higher proportion of responses in the 'Agree' and 'Strongly Agree' categories
indicates stronger consensus regarding the selected effect.

Differences in distribution patterns between genders suggest variations in how traffic
congestion impacts or is perceived by different groups, providing deeper insight beyond
average scores.
""")

# ================= 6. VIOLIN PLOT =================
st.subheader(f"6️⃣ Distribution of {chosen_effect} by Area Type")

fig7 = px.violin(
    sub,
    x="Area Type",
    y=chosen_effect,
    box=True,
    points="all"
)

st.plotly_chart(fig7, use_container_width=True)

st.markdown("""  
The violin plot illustrates the distribution of responses for the selected effect across
different area types. Wider sections indicate higher concentrations of responses at certain
Likert scores.

Area types with distributions concentrated at higher scores suggest greater perceived
severity of congestion effects. Variations between area types imply that geographic context
plays an important role in shaping congestion experiences around schools.
""")
   
