import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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

# ================= PAGE TITLE =================
st.title("Exploring Congestion Effects in School Areas")

st.markdown(
    "This dashboard explores how strongly respondents agree that congestion around schools "
    "causes accidents, time wastage, stress, lateness, environmental pollution, and fuel wastage, "
    "and how these perceptions differ by gender, status, and area type."
)

# ================= SUMMARY CARDS =================
total_resp = len(df)
area_counts = df["Area Type"].value_counts()
dominant_area = area_counts.idxmax() if len(area_counts) > 0 else "N/A"
likert_scale = "1–5"
gender_counts = df["Gender"].value_counts()
f_count = gender_counts.get("Female", gender_counts.get("Perempuan", 0))
m_count = gender_counts.get("Male", gender_counts.get("Lelaki", 0))

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Respondents", total_resp)
with c2:
    st.metric("Most Common Area Type", dominant_area)
with c3:
    st.metric("Measurement Scale", f"Likert {likert_scale}")
with c4:
    st.metric("Gender Distribution", f"F: {f_count} | M: {m_count}")

st.markdown("---")

# ================= GLOBAL FILTERS =================
st.subheader("Filters")

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    gender_filter = st.selectbox(
        "Gender",
        ["All"] + sorted(df["Gender"].dropna().unique().tolist())
    )
with col_f2:
    status_filter = st.selectbox(
        "Status",
        ["All"] + sorted(df["Status"].dropna().unique().tolist())
    )
with col_f3:
    area_filter = st.selectbox(
        "Area Type",
        ["All"] + sorted(df["Area Type"].dropna().unique().tolist())
    )

chosen_effect = st.selectbox("Focus on effect", effect_cols)

sub = df.copy()
if gender_filter != "All":
    sub = sub[sub["Gender"] == gender_filter]
if status_filter != "All":
    sub = sub[sub["Status"] == status_filter]
if area_filter != "All":
    sub = sub[sub["Area Type"] == area_filter]

st.info(f"Number of responses after filters: {len(sub)}")
if len(sub) == 0:
    st.warning("No data for this filter combination. Please change the filters.")
    st.stop()

# ================= 1. RANKING BAR CHART (EFFECTS) =================
st.subheader("1. Ranking of Congestion Effects (based on mean score)")

mean_effects = sub[effect_cols].mean().sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(
    x=mean_effects.values,
    y=mean_effects.index,
    palette="magma",
    ax=ax
)
ax.set_xlabel("Mean Likert score (1–5)")
ax.set_ylabel("")
ax.set_xlim(1, 5)
ax.set_title("Ranking of Congestion Effects")
st.pyplot(fig, clear_figure=True)

st.markdown(
    "This bar chart ranks the perceived effects of congestion from lowest to highest mean score "
    "under the current filters."
)

# ================= 2. BOX PLOTS (SELECTED EFFECT) =================
st.subheader(f"2. Distribution of **{chosen_effect}** by Gender and Status")

col_b1, col_b2 = st.columns(2)

with col_b1:
    if sub["Gender"].nunique() > 1:
        fig, ax = plt.subplots(figsize=(4, 3))
        sns.boxplot(
            data=sub,
            x="Gender",
            y=chosen_effect,
            palette=["#4c72b0", "#9ecae1"],
            ax=ax
        )
        ax.set_xlabel("Gender")
        ax.set_ylabel("Score (1–5)")
        ax.set_title("By Gender", fontsize=10)
        st.pyplot(fig, clear_figure=True)
    else:
        st.info("Only one gender present after filtering.")

with col_b2:
    if sub["Status"].nunique() > 1:
        fig, ax = plt.subplots(figsize=(4, 3))
        sns.boxplot(
            data=sub,
            x="Status",
            y=chosen_effect,
            ax=ax
        )
        ax.set_xlabel("Status")
        ax.set_ylabel("Score (1–5)")
        ax.set_title("By Status", fontsize=10)
        ax.tick_params(axis="x", rotation=30)
        st.pyplot(fig, clear_figure=True)
    else:
        st.info("Only one status present after filtering.")

# ================= 3. KEY EFFECTS BY STATUS =================
st.subheader("3. Mean scores for key effects by Status")

key_effects = [
    "Time Wastage Effect",
    "Students Late to School Effect",
    "Unintended Road Accidents Effect",
]

if sub["Status"].nunique() > 0:
    status_means = sub.groupby("Status")[key_effects].mean()

    fig, ax = plt.subplots(figsize=(7, 3.5))
    status_means.plot(
        kind="bar",
        color=sns.color_palette("Blues", len(key_effects)),
        ax=ax
    )
    ax.set_ylabel("Mean score (1–5)")
    ax.set_xlabel("Status")
    ax.tick_params(axis="x", rotation=30)
    ax.set_title("Key effects by Status", fontsize=10)
    ax.legend(title="Effect")
    st.pyplot(fig, clear_figure=True)
else:
    st.info("No status variation after filtering; grouped bar not shown.")

# ================= 4. HEATMAP =================
st.subheader("4. Correlation between causes and effects")

corr_cols = cause_cols + effect_cols
corr = sub[corr_cols].corr()

fig, ax = plt.subplots(figsize=(7, 4))
sns.heatmap(
    corr.loc[cause_cols, effect_cols],
    annot=True,
    fmt=".2f",
    cmap="Blues",
    vmin=0,
    vmax=1,
    ax=ax
)
ax.set_title("Cause–effect correlations", fontsize=10)
ax.set_xlabel("Effect variables")
ax.set_ylabel("Cause variables")
plt.xticks(rotation=30, ha="right")
st.pyplot(fig, clear_figure=True)

# ================= 5. STACKED BAR (SELECTED EFFECT) =================
st.subheader(f"5. Likert distribution of **{chosen_effect}** by Gender")

if sub["Gender"].nunique() > 1:
    dist = (
        sub.groupby("Gender")[chosen_effect]
          .value_counts(normalize=True)
          .rename("proportion")
          .reset_index()
    )

    dist_pivot = dist.pivot(index="Gender", columns=chosen_effect, values="proportion").fillna(0)
    for s in [1, 2, 3, 4, 5]:
        if s not in dist_pivot.columns:
            dist_pivot[s] = 0
    dist_pivot = dist_pivot[[1, 2, 3, 4, 5]]

    fig, ax = plt.subplots(figsize=(5.5, 3.2))
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

    ax.set_ylabel("Proportion")
    ax.set_xlabel("Gender")
    ax.set_title("Distribution of Likert scores (1–5)", fontsize=10)
    ax.set_ylim(0, 1)
    ax.legend(title="Score", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    st.pyplot(fig, clear_figure=True)
else:
    st.info("Only one gender present after filtering; stacked bar not shown.")

# ================= 6. VIOLIN PLOT BY AREA TYPE =================
st.subheader(f"6. Distribution of **{chosen_effect}** by Area Type")

if sub["Area Type"].nunique() > 0:
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.violinplot(
        data=sub,
        x="Area Type",
        y=chosen_effect,
        ax=ax
    )
    ax.set_xlabel("Area Type")
    ax.set_ylabel("Score (1–5)")
    ax.set_title(f"{chosen_effect} by Area Type", fontsize=10)
    ax.tick_params(axis="x", rotation=20)
    st.pyplot(fig, clear_figure=True)
else:
    st.info("No area type variation after filtering; violin plot not shown.")

