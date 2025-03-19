import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
import mysql.connector
from mysql.connector import Error

# Load environment variables
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Error: OPENAI_API_KEY not found. Check your .env file!")

# MySQL connection configuration from environment variables
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

# Initialize OpenAI client with the new API
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize MySQL connection
mysql_conn = None

# Initialize FastAPI
app = FastAPI(title="Catchat Backend")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.qcatchat.com", "https://qcatchat.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
)

# Define request models
class ChatCompletionRequest(BaseModel):
    model: str = "gpt-4"
    messages: list
    temperature: float = 0.7
    max_tokens: int = 1000

class ChatRequest(BaseModel):
    message: str
    mode: Optional[str] = "standard"
    quantum_computer: Optional[str] = "simulator"
    qubits: Optional[int] = 5
    user_id: Optional[str] = "1"  # Default to user_id 1 as int

def get_mysql_connection():
    global mysql_conn
    try:
        if mysql_conn is None or not mysql_conn.is_connected():
            mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
            print("MySQL connection established")
        return mysql_conn
    except Error as e:
        print(f"MySQL connection error: {e}")
        return None

def save_to_mysql(user_id, message, mode="standard", response=None):
    try:
        # Convert user_id to integer if it's a string
        if isinstance(user_id, str):
            if user_id.isdigit():
                user_id = int(user_id)
            else:
                # For non-numeric user_ids like "anonymous", use a default value of 1
                user_id = 1
                
        print(f"Attempting to save to MySQL with user_id={user_id}, message={message[:20]}...")
        conn = get_mysql_connection()
        if conn:
            cursor = conn.cursor()
            
            # Save to chat_history table
            try:
                query = """INSERT INTO chat_history (user_id, message, response) VALUES (%s, %s, %s)"""
                cursor.execute(query, (user_id, message, response))
                print("Successfully inserted into chat_history")
            except Error as e:
                print(f"Error inserting into chat_history: {e}")
                return False
            
            # Save to user_interactions table
            try:
                query = """INSERT INTO user_interactions (user_id, action_type) VALUES (%s, %s)"""
                cursor.execute(query, (user_id, f"chat_{mode}"))
                print("Successfully inserted into user_interactions")
            except Error as e:
                print(f"Error inserting into user_interactions: {e}")
                # Continue even if user_interactions fails
            
            # Save to user_preferences table
            try:
                query = """INSERT IGNORE INTO user_preferences (user_id, preferences) VALUES (%s, %s)"""
                preference_json = f'{{"mode":"{mode}"}}'
                cursor.execute(query, (user_id, preference_json))
                print("Successfully inserted into user_preferences")
            except Error as e:
                print(f"Error inserting into user_preferences: {e}")
                # Continue even if user_preferences fails
            
            conn.commit()
            cursor.close()
            return True
    except Error as e:
        print(f"Error saving to MySQL: {e}")
    return False

def format_response(raw_response: str) -> dict:
    if "Summary:" in raw_response and "Details:" in raw_response:
        try:
            summary_part = raw_response.split("Summary:")[1].split("Details:")[0].strip()
            details_part = raw_response.split("Details:")[1].strip()
            return {"summary": summary_part, "details": details_part}
        except Exception:
            pass
    return {"summary": "", "details": raw_response}

@app.get("/")
def read_root():
    return {"message": "Welcome to Catchat!"}

@app.get("/test-db")
def test_db():
    """Test endpoint to verify database saving works"""
    try:
        conn = get_mysql_connection()
        if conn:
            cursor = conn.cursor()
            
            # Test insert using an integer user_id
            query = "INSERT INTO chat_history (user_id, message, response) VALUES (%s, %s, %s)"
            cursor.execute(query, (1, "Test message from API", "Test response"))
            
            # Commit the transaction
            conn.commit()
            cursor.close()
            return {"success": True, "message": "Test data inserted successfully"}
        else:
            return {"success": False, "message": "Could not establish database connection"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/chat/{user_input}")
async def chat_get(user_input: str):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are the user interface to various Quantum Computers. You are also an helpful assistant"},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
            max_tokens=1000
        )
        raw_reply = response.choices[0].message.content.strip()
        structured_reply = format_response(raw_reply)
        
        # Save interaction to MySQL
        save_to_mysql(1, user_input, "standard", raw_reply)  # Using default user_id 1
        
        return {"response": structured_reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_post(request_data: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are the user interface to various Quantum Computers. You are also an helpful assistant"},
                {"role": "user", "content": request_data.message},
            ],
            temperature=0.7,
            max_tokens=1000
        )
        raw_reply = response.choices[0].message.content.strip()
        structured_reply = format_response(raw_reply)
        
        # Save interaction to MySQL
        user_id = request_data.user_id if hasattr(request_data, 'user_id') else "1"
        save_to_mysql(
            user_id=user_id,
            message=request_data.message,
            mode=request_data.mode,
            response=raw_reply
        )
        
        return {"response": structured_reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat/completions")
async def chat_completions(request_data: ChatCompletionRequest):
    # Implementation omitted for brevity
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
