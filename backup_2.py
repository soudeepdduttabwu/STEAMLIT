import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import sqlalchemy
# Load environment variables from the .env file
load_dotenv()
# Function to create a database connection using SQLAlchemy
def create_connection():
    try:
        user = os.getenv('USER')
        password = os.getenv('PASSWORD')
        host = os.getenv('HOST')
        port = os.getenv('PORT')
        database = os.getenv('DATABASE')

        if not all([user, password, host, port, database]):
            st.error("One or more environment variables are not set.")
            return None

        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        )
        return engine
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
        return None
# Function to fetch data from the database
def fetch_data(query, engine):
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Function to run the attendance SQL query (assuming it retrieves all records)
def run_attendance_query(start_date=None, end_date=None):
    try:
        with open("attendance.sql", "r") as file:
            query = file.read()

        # Modify the query to include start_date and end_date if provided
        if start_date and end_date:
            query = query.format(start_date=start_date, end_date=end_date)

        engine = create_connection()
        if engine:
            data = fetch_data(query, engine)
            return data
        else:
            return None
    except FileNotFoundError:
        st.error("attendance.sql file not found.")
        return None

# Function to fetch detailed employee records from the attendance_view.sql file
def fetch_detailed_employee_data(user_id, start_date=None, end_date=None):
    try:
        with open("attendance_view.sql", "r") as file:
            query = file.read()

        # Replace the placeholder with the actual user_id
        query = query.format(user_id=user_id)

        if start_date and end_date:
            query = query.format(start_date=start_date, end_date=end_date)

        engine = create_connection()
        if engine:
            data = fetch_data(query, engine)
            return data
        else:
            return None
    except FileNotFoundError:
        st.error("attendance_view.sql file not found.")
        return None
# Function to fetch detailed employee records from the absent_histoery.sql file
def run_Leave_reson_sql(start_date=None, end_date=None):
    try:
        with open("Leave_reson.sql", "r") as file:
            query = file.read()

        # Modify the query to include start_date and end_date if provided
        if start_date and end_date:
            query = query.format(start_date=start_date, end_date=end_date)

        engine = create_connection()
        if engine:
            data = fetch_data(query, engine)
            return data
        else:
            return None
    except FileNotFoundError:
        st.error("absent_history.sql file not found.")
        return None
# Streamlit app
st.set_page_config(page_title="Salesforce", layout="wide")

# Retrieve query parameters
query_params = st.query_params
user_id = query_params.get("user_id", [None])[0]

if user_id:
    # Get start_date and end_date from the query parameters
    start_date = query_params.get("start_date1", [None])[0]
    end_date = query_params.get("end_date1", [None])[0]
    #st.title("Employee Details")
    if st.button("View Details", key="view_details_button", disabled=not (start_date and end_date)):
        # Fetch attendance data for the selected employee
        attendance_data = run_attendance_query(start_date, end_date)

        if attendance_data is not None:
            st.write(attendance_data)

            # Add "View Details" button
    # if st.button("View Details", key="view_details_button", disabled=not (start_date and end_date)):
    #     if user_id:  # Check if user_id is available
    #         detailed_user_data = fetch_detailed_employee_data(user_id, start_date, end_date)
    #         if detailed_user_data is not None:
    #             st.write(detailed_user_data)
    #         else:
    #             st.error("No detailed data found.")
    #     else:
    #         st.error("No user selected.")

    #     # Add a button to go back to the main Leave Management page
    #     if st.button("Back to Leave Management"):
    #         st.query_params.clear()  # Clear query parameters to return to the main page

else:
    # Main Leave Management page
    st.title("Welcome to Salesforce Dashboard")
    st.sidebar.title("Menu")
    menu_options = ["Dashboard", "Visit History", "Leave Management", "Notice", "Logout"]
    menu_selection = st.sidebar.radio("Go to", menu_options)

    if menu_selection == "Leave Management":
        st.header("Leave Management")
        #st.write("This is the leave management page.")
        
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
        st.subheader("Attendance History")
        # Run the attendance query with the selected dates
        data = run_attendance_query(start_date, end_date)
        
        if data is not None:
            st.write(data)
        else:
            st.write("No attendance records found.")

        #Absent history section(1)

    #     st.subheader("Absent History")
    #     if st.button("View Absent History", key="view_Absent_history_button"):
    #         Absent_history_data = run_leave_history_query()

    #         if Absent_history_data is not None:
    #             st.write(Absent_history_data)

    # # Add a button to go back to the main Leave Management page
    # if st.button("Back to Absent Management"):
    #     st.query_params.clear()   # Clear query parameters to return to the main page


     # Absent history section(2)  
        st.write(f"Selected date range: {start_date} to {end_date}")
        st.subheader("leave History")
        # Run the attendance query with the selected dates
        data = run_Leave_reson_sql(start_date, end_date)
        
        if data is not None:
            st.write(data)
        else:
            st.write("No leave records found.")