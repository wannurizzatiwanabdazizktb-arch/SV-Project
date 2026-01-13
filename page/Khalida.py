import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# --------- GLOBAL STYLE ----------
st.set_page_config(layout="wide")
sns.set(style="whitegrid")

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

# =============== TITLE & DESCRIPTION ===============
st.title("Exploring Traffic Effects in Front of School Areas")

st.markdown(
    "This page explores how respondents perceive the **effects of traffic congestion** near school "
    "areas, focusing on accidents, time wastage, stress, lateness, environmental pollution, and "
    "fuel wastage across different demographic groups."
)

# =============== KPI / SURVEY OVERVIEW ===============
total_resp = len(df)
area_counts = df["Area Type"].value_counts()
dominant_area = area_counts.idxmax() if len(area_counts) > 0 else "–"
likert_scale = "1–5"
gender_counts = df["Gender"].value_counts()
f_count = gender_counts.get("Female", gender_counts.get("Perempuan", 0))
m_count = gender_counts.get("Male", gender_counts.get("Lelaki", 0))

st.subheader("📊 Survey Overview")
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Total Respondents", total_resp)
with k2:
    st.metric("Most Common Area Type", dominant_area)
with k3:
    st.metric("Measurement Scale", f"Likert {likert_scale}")
with k4:
    st.metric("Gender Distribution", f"F: {f_count} | M: {m_count}")

st.markdown("---")

# =============== FILTERS (TOP BAR) ===============
st.subheader("🎯 Filters")

fc1, fc2, fc3, fc4 = st.columns(4)
with fc1:
    gender_filter = st.selectbox(
        "Gender", ["All"] + sorted(df["Gender"].dropna().unique().tolist())
    )
with fc2:
    status_filter = st.selectbox(
        "Status", ["All"] + sorted(df["Status"].dropna().unique().tolist())
    )
with fc3:
    area_filter = st.selectbox(
        "Area Type", ["All"] + sorted(df["Area Type"].dropna().unique().tolist())
    )
with fc4:
    focus_effect = st.selectbox(
        "Focus Effect", effect_cols
    )

sub = df.copy()
if gender_filter != "All":
    sub = sub[sub["Gender"] == gender_filter]
if status_filter != "All":
    sub = sub[sub["Status"] == status_filter]
if area_filter != "All":
    sub = sub[sub["Area Type"] == area_filter]

st.caption(f"Filtered respondents: **{len(sub)}**")
if len(sub) == 0:
    st.warning("No data for this filter combination. Please change the filters.")
    st.stop()

# =============== 1. RANKING BAR CHART (LIKE EXAMPLE) ===============
st.markdown("## 1. Ranking of Congestion Effects")

mean_effects = sub[effect_cols].mean().sort_values(ascending=True)

c_rank, c_desc = st.columns([2, 1])
with c_rank:
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        x=mean_effects.values,
        y=mean_effects.index,
        palette="magma",
        ax=ax
    )
    ax.set_xlabel("Mean Likert Score (1–5)")
    ax.set_ylabel("")
    ax.set_xlim(1, 5)
    ax.set_title("Ranking of Congestion Effects (Filtered Sample)", fontsize=11)
    st.pyplot(fig, clear_figure=True)

with c_desc:
    st.markdown(
        "- Bars towards the right indicate **stronger agreement** that the effect occurs.\n"
        "- Under the current filters, effects near the top of the list are perceived as the "
        "**most serious outcomes** of congestion."
    )

# =============== 2. DISTRIBUTION OF FOCUSED EFFECT ===============
st.markdown(f"## 2. Distribution of **{focus_effect}**")

d1, d2 = st.columns(2)

with d1:
    if sub["Gender"].nunique() > 1:
        fig, ax = plt.subplots(figsize=(4.5, 3.5))
        sns.boxplot(
            data=sub,
            x="Gender",
            y=focus_effect,
            palette=["#4c72b0", "#9ecae1"],
            ax=ax
        )
        ax.set_xlabel("Gender")
        ax.set_ylabel("Score (1–5)")
        ax.set_title("By Gender", fontsize=11)
        st.pyplot(fig, clear_figure=True)
    else:
        st.info("Only one gender present after filtering.")

with d2:
    if sub["Status"].nunique() > 1:
        fig, ax = plt.subplots(figsize=(4.5, 3.5))
        sns.boxplot(
            data=sub,
            x="Status",
            y=focus_effect,
            ax=ax
        )
        ax.set_xlabel("Status")
        ax.set_ylabel("Score (1–5)")
        ax.set_title("By Status", fontsize=11)
        ax.tick_params(axis="x", rotation=30)
        st.pyplot(fig, clear_figure=True)
    else:
        st.info("Only one status present after filtering.")

st.caption("Boxplots summarise median, spread, and any outliers for the focused effect.")

# =============== 3. KEY EFFECTS BY STATUS ===============
st.markdown("## 3. Mean Scores for Key Effects by Status")

key_effects = [
    "Time Wastage Effect",
    "Students Late to School Effect",
    "Unintended Road Accidents Effect",
]

if sub["Status"].nunique() > 0:
    status_means = sub.groupby("Status")[key_effects].mean()
    fig, ax = plt.subplots(figsize=(7, 4))
    status_means.plot(
        kind="bar",
        color=sns.color_palette("crest", len(key_effects)),
        ax=ax
    )
    ax.set_ylabel("Mean score (1–5)")
    ax.set_xlabel("Status")
    ax.tick_params(axis="x", rotation=25)
    ax.set_title("Key Effects by Respondent Status", fontsize=11)
    ax.legend(title="Effect")
    st.pyplot(fig, clear_figure=True)
else:
    st.info("No status variation after filtering; grouped bar not shown.")

# =============== 4. HEATMAP: CAUSES vs EFFECTS ===============
st.markdown("## 4. Relationship Between Causes and Effects")

corr_cols = cause_cols + effect_cols
corr = sub[corr_cols].corr()

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.heatmap(
    corr.loc[cause_cols, effect_cols],
    annot=True,
    fmt=".2f",
    cmap="viridis",
    vmin=0,
    vmax=1,
    ax=ax
)
ax.set_title("Correlation Between Cause Factors and Effects", fontsize=11)
ax.set_xlabel("Effect Variables")
ax.set_ylabel("Cause Variables")
plt.xticks(rotation=30, ha="right")
st.pyplot(fig, clear_figure=True)

st.caption("Darker cells indicate stronger positive association between a cause factor and an effect.")

# =============== 5. LIKERT DISTRIBUTION BY GENDER ===============
st.markdown(f"## 5. Likert Distribution of **{focus_effect}** by Gender")

if sub["Gender"].nunique() > 1:
    dist = (
        sub.groupby("Gender")[focus_effect]
          .value_counts(normalize=True)
          .rename("proportion")
          .reset_index()
    )

    dist_pivot = dist.pivot(index="Gender", columns=focus_effect, values="proportion").fillna(0)
    for s in [1, 2, 3, 4, 5]:
        if s not in dist_pivot.columns:
            dist_pivot[s] = 0
    dist_pivot = dist_pivot[[1, 2, 3, 4, 5]]

    fig, ax = plt.subplots(figsize=(6, 3.5))
    bottom = np.zeros(len(dist_pivot))
    colors = sns.color_palette("Blues", 5)

    for i, score in enumerate(dist_pivot.columns):
        values = dist_pivot[score].values
        ax.bar(
            dist_pivot.index,
            values,
            bottom=bottom,
            label=str(score),
            color=colors[i]
        )
        bottom += values

    ax.set_ylabel("Proportion of respondents")
    ax.set_xlabel("Gender")
    ax.set_title("Distribution of Likert Scores (1–5)", fontsize=11)
    ax.set_ylim(0, 1)
    ax.legend(title="Score", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    st.pyplot(fig, clear_figure=True)
else:
    st.info("Only one gender present after filtering; stacked bar not shown.")

# =============== 6. VIOLIN PLOT BY AREA TYPE ===============
st.markdown(f"## 6. {focus_effect} by Area Type")

if sub["Area Type"].nunique() > 0:
    fig, ax = plt.subplots(figsize=(7, 3.5))
    sns.violinplot(
        data=sub,
        x="Area Type",
        y=focus_effect,
        ax=ax
    )
    ax.set_xlabel("Area Type")
    ax.set_ylabel("Score (1–5)")
    ax.set_title(f"{focus_effect} by Area Type", fontsize=11)
    ax.tick_params(axis="x", rotation=20)
    st.pyplot(fig, clear_figure=True)
else:
    st.info("No area type variation after filtering; violin plot not shown.")


