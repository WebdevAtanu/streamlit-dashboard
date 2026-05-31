import streamlit as st
import pandas as pd
import pyodbc
import plotly.express as px
from datetime import date
from streamlit_plotly_events import plotly_events
from DB import get_connection
from components.Dashboard import Dashboard

# ==========================================================================================

# Configure Streamlit application
st.set_page_config(
    page_title="Payment Dashboard",
    page_icon="💳",
    layout="wide",  # Page layout (centered or wide)
    initial_sidebar_state="collapsed",  # Sidebar state (auto, expanded, collapsed)
    # Custom menu items shown in top-right menu
    menu_items={
        "Get Help": "https://streamlit.io",
        "Report a bug": "https://github.com",
        "About": "# Employee Analytics Dashboard",
    },
)

# ==========================================================================================
# Tabs

tab1, tab2, tab3 = st.tabs(["DASHBOARD", "REPORT", "ANALYTICS"])

with tab1:
    Dashboard()

with tab2:
    st.write("Tab 2 Content")

with tab3:
    st.write("Tab 3 Content")

# ==========================================================================================
