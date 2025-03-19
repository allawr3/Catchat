import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MySQL connection configuration
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

def check_users():
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check users table
            cursor.execute("SELECT id, username FROM users LIMIT 10")
            print("Available users:")
            for user in cursor.fetchall():
                print(f"ID: {user[0]}, Username: {user[1]}")
            
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_users()
