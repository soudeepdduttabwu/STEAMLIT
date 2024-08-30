import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from sqlalchemy import text
import sqlalchemy
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
import altair as alt
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
            if data is not None:
                if sql_file == "Leave_reson.sql":
                    # Replace leave_status values with labels
                    data['leave_status'] = data['leave_status'].map({0: 'Pending', 1: 'Approved', 2: 'Rejected'})
                elif sql_file == "emp_time_spent.sql":
                    # Replace leave_status values with label
                    # Add the missing code here
                    pass
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
    #st.subheader("Attendance History")
    attendance_data = run_query("attendance.sql", start_date, end_date)
    st.subheader("Attendance History")
    attendance_data = run_query("attendance.sql", start_date, end_date)
    if attendance_data is not None:
        # Rename columns to display custom names
        attendance_data = attendance_data.rename(columns={
                'date': 'Date',
                'Name': 'Name',
                'Entry_time': 'Entry time',
                'Entry_Address': 'Entry Address',
                'Exit_time': 'Exit time',
                'Exit_Address': 'Exit Address'
            })
        display_cols = ['Date', 'Name', 'Entry time', 'Entry Address', 'Exit time', 'Exit Address']
        st.write(attendance_data[display_cols])
    else:
        st.write("No attendance records found.")

    
    # Leave History section
    st.subheader("Leave History")
    leave_data = run_query("Leave_reson.sql", start_date, end_date)
    if leave_data is not None:

    # Rename columns to display custom names
        leave_data = leave_data.rename(columns={
            'user_name': 'Employee Name',
            'Leave_mark_Date': 'Leave Date',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'reason': 'Reason',
            'leave_status': 'Leave Status'
        })
        display_cols = ['Employee Name', 'Leave Date', 'Start Date', 'End Date', 'Reason', 'Leave Status']
        st.write(leave_data[display_cols])
        #st.write(leave_data)
        # Add a dropdown to update leave status
        leave_status_options = ["Pending", "Approved", "Rejected"]
        user_name_list = leave_data['Employee Name'].tolist()  # Get the list of employee names
        selected_user_name = st.selectbox("Select Employee to Update", user_name_list)
        selected_leave_status = st.selectbox("Update Leave Status", leave_status_options)
        if st.button("Update Leave Status"):
            # Get the leave ID corresponding to the selected employee name
            selected_leave_id = leave_data.loc[leave_data['Employee Name'] == selected_user_name, 'leave_id'].iloc[0]
            # Update leave status in database
            from sqlalchemy import bindparam
            update_query = text("UPDATE git.Leave_reason SET `status` =:status WHERE `id` =:id")
            params = {
                "status": {"Pending": 0, "Approved": 1, "Rejected": 2}[selected_leave_status],
                "id": selected_leave_id
            }
            #st.write(f"Update query: {update_query} with params {params}")
            engine = create_connection()
            #if engine:
               # st.write("Database connection established successfully!")
            conn = engine.connect()
            try:
                conn.execute(update_query, params)
                conn.commit()  # Commit the changes
                conn.close()
                st.success("Leave status updated successfully!")
            except sqlalchemy.exc.DBAPIError as e:
                st.error(f"Error updating leave status: {e}")
# user time spent 

    st.header("User Time Spent")
    st.subheader("View time spent by employees")

    user_time_spent_data = run_query("emp_time_spent.sql", start_date, end_date)
    if user_time_spent_data is not None:
        # Rename columns to display custom names
        user_time_spent_data = user_time_spent_data.rename(columns={
            'name': 'Employee Name',
            'date':'DATE',
            'ENTRY_TIME':'Entry time',
            'EXIT_TIME':'Exit time',
            'TOTAL_TIME_SPENT':'Total time'
            })
        # Display the data
        display_cols1 = ['Employee Name', 'DATE', 'Total time']
        st.write(user_time_spent_data[display_cols1])
        
        # Convert 'Total time' to minutes.seconds format
        user_time_spent_data['Total time (min.sec)'] = user_time_spent_data['Total time'].apply(
            lambda x: x.total_seconds() / 60 if pd.notna(x) else 0  # Convert to minutes
        )
        
        # Pivot the data to have dates as columns and employee names as rows
        pivot_data = user_time_spent_data.pivot_table(
            index='Employee Name',
            columns='DATE',
            values='Total time (min.sec)',
            aggfunc='sum'
        ).fillna(0)  # Fill NaN values with 0
        
        # Transpose the data to have dates on the x-axis
       # pivot_data1 = pivot_data.T
        
        # Display the pivoted data (optional)
        st.write(pivot_data)
        
        # Create a bar chart
        st.bar_chart(pivot_data)
    else:
        st.write("No data found")