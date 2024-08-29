import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from sqlalchemy import text
import sqlalchemy
# Load environment variables from the .env file
load_dotenv()
# Database connection settings
def create_connection():
    try:
        user = os.getenv('USER')
        password = os.getenv('PASSWORD')
        host = os.getenv('HOST')
        port = os.getenv('PORT')
        database = os.getenv('DATABASE')
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
# Function to run SQL queries
def run_query(sql_file, start_date=None, end_date=None):
    try:
        with open(sql_file, "r") as file:
            query = file.read()

        if start_date and end_date:
            query = query.format(start_date=start_date, end_date=end_date)
        engine = create_connection()
        if engine:
            data = fetch_data(query, engine)
            if data is not None and sql_file == "Leave_reson.sql":
                # Replace leave_status values with labels
                data['leave_status'] = data['leave_status'].map({0: 'Pending', 1: 'Approved', 2: 'Rejected'})
            return data
        else:
            return None
    except FileNotFoundError:
        st.error(f"{sql_file} file not found.")
        return None
# Streamlit app
st.set_page_config(page_title="Salesforce", layout="wide")
# Main Leave Management page
st.title("Welcome to Salesforce Dashboard")
st.sidebar.title("Menu")
menu_options = ["Dashboard", "Visit History", "Leave Management", "Notice", "Logout"]
menu_selection = st.sidebar.radio("Go to", menu_options)
if menu_selection == "Leave Management":
    st.header("Leave Management")

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

    # Attendance History section
    st.subheader("Attendance History")
    attendance_data = run_query("attendance.sql", start_date, end_date)
    if attendance_data is not None:
        st.write(attendance_data)
    else:
        st.write("No attendance records found.")

    # Leave History section
    # Leave History section
    st.subheader("Leave History")
    leave_data = run_query("Leave_reson.sql", start_date, end_date)
    if leave_data is not None:
        st.write(leave_data)
        # Add a dropdown to update leave status
        leave_status_options = ["Pending", "Approved", "Rejected"]
        leave_status_selected = st.selectbox("Update Leave Status", leave_status_options)
        if leave_status_selected:
            # Update leave status in database
            from sqlalchemy import bindparam
            update_query = text("UPDATE Leave_reason SET status = :status WHERE id = :id")
            params = {
                "status": {"Pending": 0, "Approved": 1, "Rejected": 2}[leave_status_selected],
                "id": leave_data.iloc[0]['leave_id']  # Assuming the column name is 'leave_id'
            }
        update_query = update_query.bindparams(bindparam("id", params["id"]))
        conn.execute(update_query, params)
            

            