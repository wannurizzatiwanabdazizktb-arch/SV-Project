import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Crime Clustering Dashboard",
    page_icon="📊",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("📊 Crime Analytics Dashboard Menu")
    st.write("Gain insights into relationships between socioeconomic factors and crime patterns across cities.")
    st.markdown("---")
    st.subheader("📂 Navigation")
    st.info("Use the menu to explore different analysis modules.")
    st.markdown("---")
    st.caption("👩🏻‍💻 Created by **Nurul Ain Maisarah Hamidin (2025)** | Scientific Visualization Project 🌟")


def create_disagreement_heatmap(df, factor_cols, effect_cols, step_cols):
    all_likert_cols = factor_cols + effect_cols + step_cols
    heatmap_data_detailed = []

    # 1. Data Processing
    for area in ['Rural areas', 'Suburban areas', 'Urban areas']:
        for col in all_likert_cols:
            # Safely check if column exists in dataframe
            if col in df.columns:
                count_sd = df.loc[df['Area Type'] == area, col].isin([1]).sum()
                count_d  = df.loc[df['Area Type'] == area, col].isin([2]).sum()
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

    if not heatmap_data_detailed:
        st.warning("No disagreement data found to display.")
        return None

    heatmap_df_detailed = pd.DataFrame(heatmap_data_detailed)

    # 2. Ordering
    item_order = [i for i in (factor_cols + effect_cols + step_cols) if i in heatmap_df_detailed['Likert Item'].unique()]
    heatmap_df_detailed['Likert Item'] = pd.Categorical(heatmap_df_detailed['Likert Item'], categories=item_order, ordered=True)

    # 3. Pivoting
    heatmap_pivot_z = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Total Disagreement Count').fillna(0)
    heatmap_pivot_sd = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Strongly Disagree (1)').fillna(0)
    heatmap_pivot_d = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Disagree (2)').fillna(0)

    # 4. Customdata Construction
    customdata_array = np.stack([heatmap_pivot_sd.values, heatmap_pivot_d.values], axis=-1)

    # 5. Figure Creation
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot_z.values,
        x=heatmap_pivot_z.columns,
        y=heatmap_pivot_z.index,
        colorscale='YlGnBu',
        text=heatmap_pivot_z.values,
        texttemplate="%{text}",
        showscale=True,
        hovertemplate='<b>%{y}</b><br>Area: %{x}<br>Total Disagreement: %{z}<br>Strongly Disagree: %{customdata[0]}<br>Disagree: %{customdata[1]}<extra></extra>',
        customdata=customdata_array
    ))

    # Grid lines logic
    for i in range(len(heatmap_pivot_z.index)+1):
        fig.add_shape(type='line', x0=-0.5, x1=len(heatmap_pivot_z.columns)-0.5, y0=i-0.5, y1=i-0.5, line=dict(color='white', width=2))
    for j in range(len(heatmap_pivot_z.columns)+1):
        fig.add_shape(type='line', y0=-0.5, y1=len(heatmap_pivot_z.index)-0.5, x0=j-0.5, x1=j-0.5, line=dict(color='white', width=2))

    fig.update_layout(
        title="Disagreement Responses (1 & 2) Across Area Types",
        xaxis_title="Area Type",
        yaxis_title="Likert Scale Item",
        template='plotly_white',
        height=900
    )
    
    return fig

# --- STREAMLIT APP LAYOUT ---
st.title("Survey Analysis Dashboard")

# Assuming merged_df is already loaded. 
# For demonstration, I'll assume you load it here:
# merged_df = pd.read_csv("your_data.csv")

if 'merged_df' in locals() or 'merged_df' in globals():
    fig = create_disagreement_heatmap(merged_df, factor_cols, effect_cols, step_cols)
    if fig:
        # use_container_width makes the chart responsive
        st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Dataframe 'merged_df' not found. Please ensure your data is loaded.")
