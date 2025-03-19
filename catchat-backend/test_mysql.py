import mysql.connector
from mysql.connector import Error

# MySQL connection configuration
MYSQL_CONFIG = {
    'host': '82.29.153.141',  # Update with your actual host
    'user': 'allawr3',  # Update with your actual username
    'password': 'GoLightrider2024',  # Update with your actual password
    'database': 'Catchat'
}

def test_connection():
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"Connected to database: {record[0]}")
            
            # Test table existence
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print("Available tables:")
            for table in tables:
                print(f"- {table[0]}")
                
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            return True
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return False

if __name__ == "__main__":
    test_connection()
