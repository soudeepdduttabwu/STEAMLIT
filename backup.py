import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Load environment variables from the .env file
load_dotenv()

# Function to create a database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
        return connection
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
        return None

# Function to fetch data from the database
def fetch_data(query):
    connection = create_connection()
    if connection:
        df = pd.read_sql(query, connection)
        connection.close()
        return df
    else:
        return None

# Function to run the attendance SQL query with date filters
def run_attendance_query(start_date, end_date):
    try:
        with open("attendance.sql", "r") as file:
            query = file.read()
        
        # Replace placeholders in the query with actual dates
        query = query.format(start_date=start_date, end_date=end_date)
        
        # Fetch data from the database
        data = fetch_data(query)
        return data
    except FileNotFoundError:
        st.error("attendance.sql file not found.")
        return None

# Streamlit app
st.set_page_config(page_title="Salesforce", layout="wide")

st.title("Welcome to Salesforce Dashboard")

st.sidebar.title("Menu")

menu_options = ["Dashboard", "Visit History", "Attendance History", "Notice", "Logout"]

menu_selection = st.sidebar.radio("Go to", menu_options)

if menu_selection == "Attendance History":
    st.header("Attendance History")
    st.write("This is the Attendance History page.")
    
    # Create date filters
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)

    # Add custom date filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("📅Start date📅", value=today)
    with col2:
        end_date = st.date_input("📅End date📅", value=today)

    # Add "Today" and "Yesterday" shortcuts in one line
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📅Today📅"):
            start_date = today
            end_date = today
    with col2:
        if st.button("📅Yesterday📅"):
            start_date = yesterday
            end_date = yesterday
    
    # Display selected dates
    st.write(f"Selected date range: {start_date} to {end_date}")
    
    # Run the attendance query with the selected dates
    data = run_attendance_query(start_date, end_date)
    
    # Display the result in a table format
    if data is not None and not data.empty:
        st.write(data)
    else:
        st.write("No records found for the selected date range.")