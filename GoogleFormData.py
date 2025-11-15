import streamlit as st
import pandas as pd

st.header("Survey Dataset: Public Opinions on School Traffic Congestion During Peak Hours")
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8nPPwgVKnGxpQLQFTH6EQLpO6l1l2BlEAdGqmb0Bq7FGQzViLwKbb78NMjJSA1-eHl-Ebq5Wl4LRU/pub?gid=745446698&single=true&output=csv"
df = pd.read_csv(url)

# Exclude columns by name
df = df.drop(columns=["Timestamp", "Score"])

# Rename columns to fixed names
# Mapping of English column names
fixed_columns_en = {
    df.columns[0]: "Age Group",
    df.columns[1]: "Status",
    df.columns[2]: "Gender",
    df.columns[3]: "Race",
    df.columns[4]: "Area Type",
    df.columns[5]: "Rainy Weather Factor",
    df.columns[6]: "Increasing Population Factor",
    df.columns[7]: "Undisciplined Driver Factor",
    df.columns[8]: "Damaged Road Factor",
    df.columns[9]: "Students Not Sharing Vehicles",
    df.columns[10]: "Leaving Work Late Factor",
    df.columns[11]: "Narrow Road Factor",
    df.columns[12]: "Single Gate Factor",
    df.columns[13]: "Lack of Pedestrian Bridge Factor",
    df.columns[14]: "Lack of Parking Space Factor",
    df.columns[15]: "Late Drop-off/Pick-up Factor",
    df.columns[16]: "Construction/Roadworks Factor",
    df.columns[17]: "Unintended Road Accidents Effect",
    df.columns[18]: "Time Wastage Effect",
    df.columns[19]: "Pressure on Road Users Effect",
    df.columns[20]: "Students Late to School Effect",
    df.columns[21]: "Environmental Pollution Effect",
    df.columns[22]: "Fuel Wastage Effect",
    df.columns[23]: "Pedestrian Bridge Step",
    df.columns[24]: "Widening Road Step",
    df.columns[25]: "Vehicle Sharing Step",
    df.columns[26]: "Two Gates Step",
    df.columns[27]: "Arrive Early Step",
    df.columns[28]: "Traffic Officers Step",
    df.columns[29]: "Special Drop-off Area Step"
}

df_english = df.rename(columns=fixed_columns)

st.dataframe(df_english)
