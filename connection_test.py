import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def test_mysql_connection():
    connection = None  # Initialize the connection variable
    
    try:
        # Get database connection details from environment variables
        host = os.getenv("HOST")
        port = os.getenv("PORT")
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        database = os.getenv("DATABASE")

        # Check if environment variables are loaded correctly
        if not host or not user or not password or not database or not port:
            raise ValueError("Database connection details are missing. Please check your .env file.")

        # Establish the connection
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            print(f"You're connected to database: {database}")
    
    except Error as e:
        print("Error while connecting to MySQL", e)
    
    except ValueError as ve:
        print(ve)
    
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

# Test the connection
test_mysql_connection()
