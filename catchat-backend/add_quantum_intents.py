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

    # First, check if we have the "Available Quantum Systems" application in quantum_applications
    cursor.execute("SELECT id FROM quantum_applications WHERE name = 'Available Quantum Systems'")
    result = cursor.fetchone()

    if not result:
        print("Creating 'Available Quantum Systems' application...")
        cursor.execute("""
            INSERT INTO quantum_applications 
            (name, description, requires_randomness, qubit_count, created_at)
            VALUES ('Available Quantum Systems', 'Information about available quantum computers', 0, 0, NOW())
        """)
        conn.commit()
        cursor.execute("SELECT id FROM quantum_applications WHERE name = 'Available Quantum Systems'")
        result = cursor.fetchone()

    quantum_systems_app_id = result[0]
    print(f"Found quantum systems application with ID: {quantum_systems_app_id}")

    # New patterns to add - comprehensive list for catching quantum capability questions
    new_patterns = [
        # Basic capability questions
        ("what.{1,10}quantum.{1,20}(capabilities|systems|computers)", quantum_systems_app_id, 0.9, None),
        ("(capabilities|systems).{1,10}quantum", quantum_systems_app_id, 0.9, None),
        ("(do|can).{1,10}(you|access).{1,20}quantum", quantum_systems_app_id, 0.9, None),
        ("quantum.{1,10}access", quantum_systems_app_id, 0.9, None),
        
        # Specific system questions
        ("(list|available|which).{1,10}quantum.{1,20}(systems|computers)", quantum_systems_app_id, 0.95, None),
        ("quantum.{1,5}(hardware|processors|qubits)", quantum_systems_app_id, 0.9, None),
        
        # Direct mentions of quantum computers
        ("tell.{1,10}about.{1,10}quantum.{1,10}(systems|computers)", quantum_systems_app_id, 0.95, None),
        ("quantum.{1,5}information", quantum_systems_app_id, 0.85, None),
        
        # Direct questions
        ("what.{1,10}quantum.{1,10}(computers|systems).{1,10}(available|exist|have)", quantum_systems_app_id, 0.95, None),
        ("how.{1,10}(many|much).{1,10}(quantum|qubits)", quantum_systems_app_id, 0.9, None)
    ]

    # Add new patterns
    added_count = 0
    for pattern, app_id, confidence, param_pattern in new_patterns:
        # Check if pattern already exists
        cursor.execute(
            "SELECT id FROM quantum_intent_mapping WHERE intent_pattern = %s AND quantum_application_id = %s", 
            (pattern, app_id)
        )
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO quantum_intent_mapping 
                (intent_pattern, quantum_application_id, confidence_threshold, parameter_extraction_pattern, created_at)
                VALUES (%s, %s, %s, %s, NOW())
            """, (pattern, app_id, confidence, param_pattern))
            print(f"Added new pattern: {pattern}")
            added_count += 1
        else:
            print(f"Pattern already exists: {pattern}")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Quantum intent patterns updated successfully! Added {added_count} new patterns.")
    
except mysql.connector.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")
