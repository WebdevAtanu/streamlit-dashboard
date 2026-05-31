# Streamlit Features Demo
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date, datetime

# Set page configuration for the Streamlit app
st.set_page_config(
    page_title="Streamlit Features Demo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and Header Example
st.title("🚀 Streamlit Complete Features Demo")
st.header("Header Example")
st.subheader("Subheader Example")
st.text("Simple Text")
st.markdown("**Markdown Bold Text**")
st.caption("This is a caption")
st.code("print('Hello Streamlit')", language="python")
st.divider()

# Sidebar Example for Navigation
st.sidebar.title("📌 Sidebar")
sidebar_option = st.sidebar.selectbox(
    "Select Option", ["Home", "Dashboard", "Settings"]
)

st.sidebar.success(f"Selected: {sidebar_option}")

# User Inputs Example
st.header("📝 User Inputs")

name = st.text_input("Enter Name")
password = st.text_input("Enter Password", type="password")
age = st.number_input("Enter Age", min_value=1, max_value=100)
price = st.slider("Select Price", 0, 10000, 500)
city = st.selectbox("Select City", ["Kolkata", "Delhi", "Mumbai"])
hobbies = st.multiselect("Select Hobbies", ["Coding", "Gaming", "Music", "Sports"])
gender = st.radio("Select Gender", ["Male", "Female"])
agree = st.checkbox("I Agree")
birth_date = st.date_input("Select Date", value=date.today())
time_value = st.time_input("Select Time")
color = st.color_picker("Pick Color")

uploaded_file = st.file_uploader("Upload File", type=["csv", "txt", "png", "jpg"])

if st.button("Submit"):
    st.success("Form Submitted Successfully")
    st.write("Name:", name)
    st.write("Age:", age)
    st.write("City:", city)

st.divider()

# Form Example
st.header("📋 Form Example")

with st.form("user_form"):

    user_name = st.text_input("User Name")
    user_salary = st.number_input("Salary", min_value=0)

    form_submit = st.form_submit_button("Save")

    if form_submit:
        st.success("User Saved")
        st.write(user_name, user_salary)

st.divider()

# Dataframe example
st.header("📊 DataFrame Example")

# Sample DataFrame
np.random.seed(42)

df = pd.DataFrame(
    {
        "Name": ["Sam", "John", "David", "Alex"],
        "Age": [25, 30, 35, 28],
        "Salary": [50000, 70000, 90000, 65000],
    }
)

st.dataframe(df, use_container_width=True)
st.table(df)

st.divider()

# Metrics Example
st.header("📈 Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Users", len(df))

with col2:
    st.metric("Average Age", round(df["Age"].mean(), 2))

with col3:
    st.metric("Total Salary", f"₹ {df['Salary'].sum()}")

st.divider()

# Charts Example
st.header("📉 Charts")

# Bar Chart
bar_fig = px.bar(df, x="Name", y="Salary", color="Name", title="Salary Chart")

st.plotly_chart(bar_fig, use_container_width=True)

# Pie Chart
pie_fig = px.pie(df, names="Name", values="Salary", title="Salary Distribution")

st.plotly_chart(pie_fig, use_container_width=True)

# Line Chart
line_df = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])

st.line_chart(line_df)

# Area Chart
st.area_chart(line_df)

# Bar Chart Built-in
st.bar_chart(line_df)

st.divider()

# Media Example
st.header("🖼️ Media")

st.image(
    "https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png",
    width=300,
)

st.video("https://www.youtube.com/watch?v=VqgUkExPvLY")

st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

st.divider()

# Layouts Example
st.header("📐 Layouts")

col1, col2 = st.columns(2)

with col1:
    st.info("Left Column")

with col2:
    st.warning("Right Column")

# Tabs

tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

with tab1:
    st.write("Tab 1 Content")

with tab2:
    st.write("Tab 2 Content")

with tab3:
    st.write("Tab 3 Content")

# Expander
with st.expander("See More"):
    st.write("Hidden Content")

st.divider()

# Status Messages
st.header("✅ Status Messages")

st.success("Success Message")
st.error("Error Message")
st.warning("Warning Message")
st.info("Information Message")

st.divider()

# Progress and Spinner
st.header("⏳ Progress")

progress = st.progress(50)

with st.spinner("Loading..."):
    pass

st.divider()

# Session State Example
st.header("🧠 Session State")

if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("Increase Counter"):
    st.session_state.counter += 1

st.write("Counter:", st.session_state.counter)

st.divider()

# Download Button Example
st.header("⬇️ Download File")

csv = df.to_csv(index=False)

st.download_button(
    label="Download CSV", data=csv, file_name="users.csv", mime="text/csv"
)

st.divider()

# Json Example
st.header("🧾 JSON")

sample_json = {"name": "Sam", "age": 25, "city": "Kolkata"}

st.json(sample_json)

st.divider()

# Cache Example
st.header("⚡ Cache")


@st.cache_data
def expensive_function():
    return "Cached Data"


st.write(expensive_function())

st.divider()

# Dynamic Content Example
st.header("📦 Placeholder")

placeholder = st.empty()
placeholder.success("Dynamic Content")

st.divider()

# Map Example
st.header("🗺️ Map")

map_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [22.5726, 88.3639], columns=["lat", "lon"]
)

st.map(map_data)

st.divider()

# Footer
st.success("🎉 Streamlit Features Demo Completed")
