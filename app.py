import streamlit as st

st.set_page_config(page_title="Traffic Congestion During Peak Hours in Front of Schools Dashboard")

# Import pages
page1 = st.Page("Disagreement_Traffic.py", title="Disagreement Traffic Congestion Survey")
page2 = st.Page("Izzati.py", title="Traffic Congestion Survey")
page3 = st.Page("Fathin.py", title="Traffic Congestion Survey")
page3 = st.Page("Khalida.py", title="Traffic Congestion Survey")

# Navigation
navigation = st.navigation(
    {
        "Traffic Congestion During Peak Hours in Front of Schools Dashboard": [page1, page2, page3, page4]
    }
)

navigation.run()
