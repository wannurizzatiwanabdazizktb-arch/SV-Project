import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set(style="whitegrid")

@st.cache_data
def load_data():
    df = pd.read_csv("traffic_survey.csv")
    # drop index column if it exists
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

# ---------- PAGE HEADER ----------
st.header("Effects of School-area Congestion")

st.markdown("""
Investigate how strongly respondents agree that congestion around schools causes accidents, time
wastage, stress, lateness, environmental pollution, and fuel wastage, and how these perceptions
differ by gender, status, and area type.
""")

# ---------- FILTERS ----------
col1, col2 = st.columns(2)
with col1:
    gender_filter = st.selectbox(
        "Filter by Gender (Goal 2)",
        ["All"] + sorted(df["Gender"].dropna().unique().tolist())
    )
with col2:
    status_filter = st.selectbox(
        "Filter by Status (Goal 2)",
        ["All"] + sorted(df["Status"].dropna().unique().tolist())
    )

sub = df.copy()
if gender_filter != "All":
    sub = sub[sub["Gender"] == gender_filter]
if status_filter != "All":
    sub = sub[sub["Status"] == status_filter]

st.write(f"Number of responses used in Goal 2: {len(sub)}")

# ---------- 1) SUMMARY + BAR ----------
st.subheader("1. Summary of effect scores")

mean_effects = sub[effect_cols].mean()
std_effects = sub[effect_cols].std()

summary_df = pd.DataFrame({
    "Mean": mean_effects.round(2),
    "Std": std_effects.round(2),
}).sort_values("Mean", ascending=False)

st.dataframe(summary_df)

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(
    x=summary_df["Mean"].values,
    y=summary_df.index,
    palette="Blues_r",
    ax=ax
)
ax.set_xlabel("Mean score (1–5)")
ax.set_ylabel("")
ax.set_title("Overall mean effect scores")
st.pyplot(fig)

st.markdown(
    "Most effects have mean scores above 4.0, indicating strong agreement that "
    "congestion leads to serious negative outcomes."
)

# ---------- 2) BOX PLOTS BY GENDER ----------
st.subheader("2. Effect distributions by Gender (boxplots)")

if sub["Gender"].nunique() > 1:
    fig, axes = plt.subplots(2, 3, figsize=(12, 6))
    axes = axes.flatten()
    for i, col in enumerate(effect_cols):
        sns.boxplot(
            data=sub,
            x="Gender",
            y=col,
            palette=["#4c72b0", "#9ecae1"],
            ax=axes[i]
        )
        axes[i].set_xlabel("")
        axes[i].set_ylabel("")
        axes[i].set_title(col, fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info("Only one gender present after filtering; boxplot by gender not shown.")

st.markdown(
    "Boxplots show how tightly or widely scores are spread for each gender, beyond just the means."
)

# ---------- 3) GROUPED BAR BY STATUS ----------
st.subheader("3. Mean key effects by Status (grouped bar)")

selected_effects = [
    "Time Wastage Effect",
    "Students Late to School Effect",
    "Unintended Road Accidents Effect",
]

if sub["Status"].nunique() > 0:
    status_means = sub.groupby("Status")[selected_effects].mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    status_means.plot(
        kind="bar",
        color=sns.color_palette("Blues", len(selected_effects)),
        ax=ax
    )
    ax.set_ylabel("Mean score (1–5)")
    ax.set_xlabel("Status")
    ax.tick_params(axis="x", rotation=45)
    ax.set_title("Mean scores for key effects by Status")
    ax.legend(title="Effect")
    st.pyplot(fig)
else:
    st.info("No status variation after filtering; grouped bar not shown.")

st.markdown(
    "Parents and teachers may rate student-related impacts higher, reflecting their concern for "
    "safety and punctuality."
)

# ---------- 4) HEATMAP: CAUSES VS EFFECTS ----------
st.subheader("4. Correlation between causes and effects (heatmap)")

corr_cols = cause_cols + effect_cols
corr = sub[corr_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(
    corr.loc[cause_cols, effect_cols],
    annot=True,
    fmt=".2f",
    cmap="Blues",
    vmin=0,
    vmax=1,
    ax=ax
)
ax.set_title("Correlation between causes and effects of congestion")
ax.set_xlabel("Effect variables")
ax.set_ylabel("Cause variables")
st.pyplot(fig)

st.markdown(
    "Higher correlations suggest that where certain causes are perceived as serious, "
    "respondents also report stronger negative effects."
)

# ---------- 5) STACKED BAR BY GENDER ----------
st.subheader("5. Distribution of 'Students Late to School Effect' scores by Gender (stacked bar)")

target = "Students Late to School Effect"

if sub["Gender"].nunique() > 1:
    dist = (
        sub.groupby("Gender")[target]
          .value_counts(normalize=True)
          .rename("proportion")
          .reset_index()
    )

    dist_pivot = dist.pivot(index="Gender", columns=target, values="proportion").fillna(0)
    for s in [1, 2, 3, 4, 5]:
        if s not in dist_pivot.columns:
            dist_pivot[s] = 0
    dist_pivot = dist_pivot[[1, 2, 3, 4, 5]]

    fig, ax = plt.subplots(figsize=(8, 5))
    bottom = np.zeros(len(dist_pivot))
    colors = sns.color_palette("Blues", 5)

    for i, score in enumerate(dist_pivot.columns):
        values = dist_pivot[score].values
        ax.bar(
            dist_pivot.index,
            values,
            bottom=bottom,
            label=f"Score {score}",
            color=colors[i]
        )
        bottom += values

    ax.set_ylabel("Proportion of respondents")
    ax.set_xlabel("Gender")
    ax.set_title(f"Distribution of '{target}' scores by Gender")
    ax.set_ylim(0, 1)
    ax.legend(title="Likert score", bbox_to_anchor=(1.05, 1), loc="upper left")
    st.pyplot(fig)
else:
    st.info("Only one gender present after filtering; stacked bar not shown.")

st.markdown(
    "This shows whether one gender gives more extreme scores (for example, more 5s) "
    "on students being late."
)

# ---------- 6) VIOLIN PLOT BY AREA TYPE ----------
st.subheader("6. Distribution of 'Time Wastage Effect' by Area Type (violin plot)")

target_violin = "Time Wastage Effect"

if sub["Area Type"].nunique() > 0:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.violinplot(
        data=sub,
        x="Area Type",
        y=target_violin,
        ax=ax
    )
    ax.set_xlabel("Area Type")
    ax.set_ylabel("Score (1–5)")
    ax.set_title(f"Distribution of '{target_violin}' by Area Type")
    ax.tick_params(axis="x", rotation=20)
    st.pyplot(fig)
else:
    st.info("No area type variation after filtering; violin plot not shown.")

st.markdown(
    "The violin plot reveals how responses for time wastage are distributed across rural, "
    "suburban, and urban areas."
)
