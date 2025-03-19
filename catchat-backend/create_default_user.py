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

def create_default_user():
    try:
        print("Connecting to MySQL...")
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        
        if connection.is_connected():
            print("Connection successful!")
            cursor = connection.cursor()
            
            # Create a default user
            print("Creating default user...")
            query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, ("default_user", "default@example.com", "password123"))
            
            # Commit and close
            connection.commit()
            print(f"User created successfully! User ID: {cursor.lastrowid}")
            
            # Verify by selecting the data
            cursor.execute("SELECT id, username FROM users")
            users = cursor.fetchall()
            print("Available users:")
            for user in users:
                print(f"ID: {user[0]}, Username: {user[1]}")
            
            cursor.close()
            connection.close()
            print("MySQL connection closed")
            return cursor.lastrowid
    except Error as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    user_id = create_default_user()
    print(f"Created user with ID: {user_id}")
