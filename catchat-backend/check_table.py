import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MySQL connection configuration from environment variables
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

def check_table_structure():
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check chat_history structure
            cursor.execute("DESCRIBE chat_history;")
            print("chat_history table structure:")
            for column in cursor.fetchall():
                print(column)
            
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_table_structure()
