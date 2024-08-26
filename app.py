import streamlit as st
import pandas as pd

# Set page title
st.set_page_config(page_title="My Streamlit App")

# Add a title
st.title("Welcome to My Streamlit App 😁!")

# Add a subheader
st.subheader("This is a subheader")

# Add some text
st.write("This is some regular text.")

# Add a button
if st.button("Click me!"):
    st.write("You clicked the button!")

# Add a slider
value = st.slider("Select a value", 0, 100, 50)
st.write(f"You selected {value}")

# Add a file uploader
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

# Add a selectbox
options = ["Option 1", "Option 2", "Option 3"]
selected_option = st.selectbox("Select an option", options)
st.write(f"You selected {selected_option}")

# Add a sidebar
st.sidebar.title("Sidebar")
st.sidebar.write("This is the sidebar.")

# Add a checkbox
agree = st.sidebar.checkbox("I agree")
if agree:
    st.sidebar.write("You agreed.")