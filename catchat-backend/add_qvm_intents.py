import mysql.connector
import getpass

# Get database credentials
print("Please enter database credentials:")
db_host = input("Database host (default: localhost): ") or "localhost"
db_user = input("Database username: ")
db_password = getpass.getpass("Database password: ")
db_name = input("Database name: ")

# MySQL connection configuration
MYSQL_CONFIG = {
    'host': db_host,
    'user': db_user,
    'password': db_password,
    'database': db_name
}

# Connect to database
try:
    print("Connecting to database...")
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    print("Connected successfully!")

    # Get quantum systems application ID
    cursor.execute("SELECT id FROM quantum_applications WHERE name = 'Available Quantum Systems'")
    result = cursor.fetchone()
    
    if not result:
        print("Error: 'Available Quantum Systems' application not found!")
        exit(1)
        
    quantum_app_id = result[0]
    print(f"Found quantum application ID: {quantum_app_id}")
    
    # Add abbreviation patterns
    new_patterns = [
        # QVM specific patterns
        ("qvm'?s", quantum_app_id, 0.9, None),
        ("quantum virtual machine", quantum_app_id, 0.95, None),
        ("(access|use).{1,15}(qvm|quantum.{1,5}virtual)", quantum_app_id, 0.95, None),
        
        # Other common abbreviations
        ("(access|use).{1,15}(qpu|quantum.{1,5}processing)", quantum_app_id, 0.95, None),
        ("(access|have|use).{1,15}quantum", quantum_app_id, 0.85, None),
        
        # Very simple catch-all patterns (may need tuning)
        ("\\bqvm\\b", quantum_app_id, 0.9, None),  # word boundary for QVM
        ("\\bqpu\\b", quantum_app_id, 0.9, None),  # word boundary for QPU
        ("\\bquantum\\b", quantum_app_id, 0.8, None)  # simple quantum mention
    ]
    
    # Insert new patterns
    for pattern, app_id, conf, param in new_patterns:
        cursor.execute(
            "SELECT id FROM quantum_intent_mapping WHERE intent_pattern = %s",
            (pattern,)
        )
        if cursor.fetchone():
            print(f"Pattern already exists: {pattern}")
        else:
            cursor.execute(
                "INSERT INTO quantum_intent_mapping (intent_pattern, quantum_application_id, confidence_threshold, parameter_extraction_pattern) VALUES (%s, %s, %s, %s)",
                (pattern, app_id, conf, param)
            )
            print(f"Added pattern: {pattern}")
    
    conn.commit()
    print("Successfully added QVM patterns to database!")
    
except mysql.connector.Error as err:
    print(f"MySQL Error: {err}")
except Exception as err:
    print(f"Error: {err}")
finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()
