import pyodbc
import streamlit as st


# DATABASE CONNECTION
@st.cache_resource # Cache the connection to reuse across app runs
def get_connection():

    # Establish a connection to the SQL Server database using pyodbc
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LAPTOP-P06NSLHF\SQLEXPRESS;"
        "DATABASE=streamlit-dashboard;"
        "UID=sa;"
        "PWD=admin;"
    )

    return conn
