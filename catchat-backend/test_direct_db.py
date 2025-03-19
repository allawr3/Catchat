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

def test_insert():
    try:
        print("Connecting to MySQL...")
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        
        if connection.is_connected():
            print("Connection successful!")
            cursor = connection.cursor()
            
            # Insert test data
            print("Inserting test data...")
            query = "INSERT INTO chat_history (user_id, message, response) VALUES (%s, %s, %s)"
            cursor.execute(query, (1, "Direct test message", "Direct test response"))
            
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
    test_insert()
