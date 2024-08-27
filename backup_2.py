#attemdance view all #

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

# Function to fetch detailed employee records from the attendance_view.sql file
def fetch_detailed_employee_data(user_id, start_date, end_date):
    try:
        with open("attendance_view.sql", "r") as file:
            query = file.read()

        # Replace placeholders in the SQL query with the actual user_id, start_date, and end_date
        query = query.format(user_id=user_id, start_date=start_date, end_date=end_date)

        # Fetch data from the database
        data = fetch_data(query)
        return data
    except FileNotFoundError:
        st.error("attendance_view.sql file not found.")
        return None

# Streamlit app
st.set_page_config(page_title="Salesforce", layout="wide")

# Retrieve query parameters
query_params = st.experimental_get_query_params()
user_id = query_params.get("user_id", [None])[0]

if user_id:
    # Get start_date and end_date from the query parameters
    start_date = query_params.get("start_date", [None])[0]
    end_date = query_params.get("end_date", [None])[0]
    
    if start_date is not None and end_date is not None:
        # Fetch detailed data for the selected employee
        detailed_data = fetch_detailed_employee_data(user_id, start_date, end_date)

        if detailed_data is not None:
            st.write(detailed_data)
        else:
            st.write("No records found.")
    else:
        st.error("Date range not provided.")
    
    # Add a button to go back to the main Leave Management page
    if st.button("Back to Leave Management"):
        st.experimental_set_query_params()  # Clear query parameters to return to the main page

else:
    # Main Leave Management page
    st.title("Welcome to Salesforce Dashboard")
    st.sidebar.title("Menu")
    menu_options = ["Dashboard", "Visit History", "Leave Management", "Notice", "Logout"]
    menu_selection = st.sidebar.radio("Go to", menu_options)

    if menu_selection == "Leave Management":
        st.header("Leave Management")
        st.write("This is the leave management page.")
        
        # Create date filters
        today = datetime.today().date()
        yesterday = today - timedelta(days=1)

        # Add custom date filter
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date", value=today)
        with col2:
            end_date = st.date_input("End date", value=today)

        # Add "Today" and "Yesterday" shortcuts in one line
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Today"):
                start_date = today
                end_date = today
        with col2:
            if st.button("Yesterday"):
                start_date = yesterday
                end_date = yesterday
        
        # Display selected dates
        st.write(f"Selected date range: {start_date} to {end_date}")

        # Run the attendance query with the selected dates
        data = run_attendance_query(start_date, end_date)

        if data is not None:
            st.subheader(f"Attendance Records from {start_date} to {end_date}")

            # Display the result in a table format with "View" buttons
            for index, row in data.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Name**: {row['Name']}, **Entry Time**: {row['Entry_time']}, **Exit Time**: {row['Exit_time']}")
                with col2:
                    # Pass start_date and end_date when calling the function
                    if st.button(f"View", key=f"view_{index}"):
                        st.experimental_set_query_params(user_id=row['user_id'], name=row['Name'], start_date=str(start_date), end_date=str(end_date))
