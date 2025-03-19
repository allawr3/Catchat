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

def test_insert_with_user(user_id):
    try:
        print(f"Connecting to MySQL with user_id={user_id}...")
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        
        if connection.is_connected():
            print("Connection successful!")
            cursor = connection.cursor()
            
            # Insert test data with the valid user_id
            print(f"Inserting test data with user_id={user_id}...")
            query = "INSERT INTO chat_history (user_id, message, response) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, "Test with valid user ID", "Test response"))
            
            # Commit and close
            connection.commit()
            print(f"Insertion successful! Affected rows: {cursor.rowcount}")
            
            # Verify by selecting the data
            cursor.execute("SELECT * FROM chat_history ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
            print(f"Last inserted row: {result}")
            
            cursor.close()
            connection.close()
            print("MySQL connection closed")
            return True
    except Error as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Use the ID from the user you created - replace 1 with your actual user ID
    test_insert_with_user(1)
