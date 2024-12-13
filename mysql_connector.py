import mysql.connector
from mysql.connector import Error

def connect_to_database():
    """Connect to the database and return the connection object."""
    try:
        print("Attempting to connect to the database...")
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your database host
            user='root',  # Replace with your database username
            password='May12003',  # Replace with your database password
            database='project'  # Replace with your database name
        )
        if connection.is_connected():
            print("Successfully connected to the database.")
            return connection
        else:
            print("Connection failed.")
    except Error as e:
        print(f"Error connecting to the database: {e}")
    return None

if __name__ == "__main__":
    connect_to_database()
