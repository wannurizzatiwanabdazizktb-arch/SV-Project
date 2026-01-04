import streamlit as st

st.set_page_config(
    page_title="Traffic Congestion Dashboard",
    layout="wide"
)

# Define pages (MAKE SURE PATH IS CORRECT)
page1 = st.Page(
    "page/Disagreement_Traffic.py",
    title="Disagreement Traffic Congestion Survey",
    icon="📊"
)

page2 = st.Page(
    "page/Izzati.py",
    title="Traffic Congestion Survey – Izzati",
    icon="📈"
)

page3 = st.Page(
    "page/Fathin.py",
    title="Traffic Congestion Survey – Fathin",
    icon="📉"
)

page4 = st.Page(
    "page/Khalida.py",
    title="Traffic Congestion Survey – Khalida",
    icon="📌"
)

# Navigation
navigation = st.navigation(
    {
        "Traffic Congestion During Peak Hours in Front of Schools Dashboard": [
            page1,
            page2,
            page3,
            page4
        ]
    }
)

navigation.run()
