import os
import openai
import json
import time
import tempfile
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from io import BytesIO
import mysql.connector
from mysql.connector import Error
import re
import hashlib
import uuid
from functools import lru_cache
from weather_client import WeatherClient
import logging

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/root/catchat-backend/backend.log',
    filemode='a'
)
logger = logging.getLogger("catchat")

def get_location_from_ip(ip_address):
    """Get location from IP address using a free geolocation API"""
    try:
        logger.info(f"Looking up location for IP: {ip_address}")

        # Skip localhost and private IPs
        if ip_address in ['127.0.0.1', 'localhost'] or ip_address.startswith(('192.168.', '10.', '172.16.')):
            logger.warning(f"Skipping local/private IP: {ip_address}")
            return "New York"  # Default fallback for development

        # Use ipinfo.io API (free tier)
        import requests
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")

        if response.status_code == 200:
            data = response.json()

            # ipinfo.io returns city and region
            city = data.get('city')
            region = data.get('region')
            country = data.get('country')

            if city:
                if country == 'US' and region:
                    location = f"{city}, {region}"
                else:
                    location = city

                logger.info(f"Found location from IP: {location}")
                return location
            else:
                logger.warning(f"No city found in IP data: {data}")
                return None
        else:
            logger.error(f"IP lookup failed with status: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"Error in IP geolocation: {e}", exc_info=True)
        return None

def convert_to_us_units(weather_data):
    """Convert weather data from metric to US units"""
    if not weather_data:
        return weather_data
    
    converted = weather_data.copy()
    
    # Convert temperature from Celsius to Fahrenheit
    if 'temperature' in converted:
        converted['temperature_f'] = round((converted['temperature'] * 9/5) + 32, 1)
    
    if 'feels_like' in converted:
        converted['feels_like_f'] = round((converted['feels_like'] * 9/5) + 32, 1)
    
    # Convert wind speed from km/h to mph
    if 'wind_speed' in converted:
        converted['wind_speed_mph'] = round(converted['wind_speed'] * 0.621371, 1)
    
    return converted

# Log startup
logger.info("====== APPLICATION STARTING ======")

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("Error: OPENAI_API_KEY not found. Check your .env file!")
    raise ValueError("Error: OPENAI_API_KEY not found. Check your .env file!")

# MySQL connection configuration from environment variables
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

logger.info(f"MySQL configuration: host={MYSQL_CONFIG['host']}, database={MYSQL_CONFIG['database']}")

# Initialize OpenAI client with the new API
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize MySQL connection
mysql_conn = None

# Initialize FastAPI
app = FastAPI(title="Catchat Backend")

# Initialize the weather client
weather_client = WeatherClient(base_url="http://localhost:8001")  # Adjust URL as needed

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
    user_id: Optional[str] = "1"  # Default to user_id 1

def get_mysql_connection():
    global mysql_conn
    try:
        if mysql_conn is None or not mysql_conn.is_connected():
            logger.info("Establishing new MySQL connection")
            mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
            logger.info("MySQL connection established successfully")
        return mysql_conn
    except Error as e:
        logger.error(f"MySQL connection error: {e}")
        return None

def get_valid_user_id(user_id="1"):
    """Get a valid user ID from the database"""
    try:
        logger.debug(f"Validating user_id: {user_id}")
        # Convert to integer if possible
        if isinstance(user_id, str) and user_id.isdigit():
            user_id = int(user_id)
        else:
            # Use default user
            user_id = 1
            logger.debug("Using default user_id: 1")

        # Verify user exists
        conn = get_mysql_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()

            if result:
                logger.debug(f"Valid user_id found: {user_id}")
                cursor.close()
                return user_id
            else:
                # Check if any users exist
                cursor.execute("SELECT id FROM users LIMIT 1")
                result = cursor.fetchone()

                if result:
                    logger.debug(f"Using first available user_id: {result[0]}")
                    cursor.close()
                    return result[0]
                else:
                    # No users found - create default user
                    logger.warning("No users found in database, creating default user")
                    try:
                        cursor.execute("""
                            INSERT INTO users (id, username, email, created_at)
                            VALUES (1, 'default_user', 'default@example.com', NOW())
                            ON DUPLICATE KEY UPDATE username = 'default_user'
                        """)
                        conn.commit()
                        logger.info("Created default user with ID 1")
                        cursor.close()
                        return 1
                    except Exception as e:
                        logger.error(f"Error creating default user: {e}")
                        cursor.close()
                        return 1  # Return 1 anyway as fallback
    except Error as e:
        logger.error(f"Error finding valid user: {e}")
    return 1  # Always fall back to user ID 1

def save_to_mysql(user_id, message, mode="standard", response=None):
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        try:
            logger.debug(f"Saving to MySQL - user_id: {user_id}, mode: {mode} (attempt {attempts+1})")
            # Get valid user ID
            valid_user_id = get_valid_user_id(user_id)

            conn = get_mysql_connection()
            if conn:
                cursor = conn.cursor()

                # Save to chat_history table
                try:
                    query = """INSERT INTO chat_history (user_id, message, response) VALUES (%s, %s, %s)"""
                    cursor.execute(query, (valid_user_id, message, response))
                    logger.info(f"Successfully inserted into chat_history for user {valid_user_id}")
                except Error as e:
                    logger.error(f"Error inserting into chat_history: {e}")
                    if "Lock wait timeout exceeded" in str(e) and attempts < max_attempts - 1:
                        attempts += 1
                        cursor.close()
                        time.sleep(1)  # Wait before retry
                        continue
                    else:
                        cursor.close()
                        return False

                # Continue with other operations...
                # Rest of the function remains the same

                conn.commit()
                cursor.close()
                return True

        except Error as e:
            logger.error(f"Error saving to MySQL: {e}")
            if "Lock wait timeout exceeded" in str(e) and attempts < max_attempts - 1:
                attempts += 1
                time.sleep(1)  # Wait before retry
                continue
            else:
                return False

        # If we get here, we've completed successfully
        break

    return False

def format_response(raw_response: str) -> dict:
    if "Summary:" in raw_response and "Details:" in raw_response:
        try:
            summary_part = raw_response.split("Summary:")[1].split("Details:")[0].strip()
            details_part = raw_response.split("Details:")[1].strip()
            return {"summary": summary_part, "details": details_part}
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
    return {"summary": "", "details": raw_response}

def detect_quantum_intent(message):
    """Detect if message contains intent for quantum application"""
    try:
        logger.debug(f"Detecting quantum intent for message: {message}")
        conn = get_mysql_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)

            # Get all intent patterns
            cursor.execute("SELECT * FROM quantum_intent_mapping")
            intents = cursor.fetchall()
            cursor.close()

            message_lower = message.lower()
            logger.debug(f"Found {len(intents)} intent patterns to check")

            # Check each intent pattern
            for intent in intents:
                if re.search(intent['intent_pattern'], message_lower, re.IGNORECASE):
                    logger.info(f"Quantum intent detected: {intent['quantum_application_id']}")
                    # Extract parameters if pattern exists
                    params = None
                    if intent['parameter_extraction_pattern']:
                        param_match = re.search(intent['parameter_extraction_pattern'], message, re.IGNORECASE)
                        if param_match:
                            params = param_match.group(1)

                    return {
                        'application_id': intent['quantum_application_id'],
                        'confidence': intent['confidence_threshold'],
                        'parameters': params
                    }

        logger.debug("No quantum intent detected")
        return None
    except Exception as e:
        logger.error(f"Error detecting quantum intent: {e}")
        return None

@lru_cache(maxsize=32)
def get_available_quantum_systems():
    """Retrieve information about available quantum systems"""
    try:
        logger.info("Fetching available quantum systems from database")
        conn = get_mysql_connection()
        if not conn:
            logger.error("Failed to establish MySQL connection")
            return None

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            system_name as name,
            qubit_count as qubits,
            system_type as type,
            is_free,
            requires_api_key,
            description
        FROM quantum_systems_catalog
        ORDER BY is_free DESC, qubit_count DESC
        """

        cursor.execute(query)
        systems = cursor.fetchall()
        cursor.close()

        logger.info(f"Successfully retrieved {len(systems)} quantum systems from database")

        # Format for response
        result = {
            "systems": systems,
            "total_count": len(systems),
            "free_systems_count": sum(1 for s in systems if s['is_free']),
            "paid_systems_count": sum(1 for s in systems if not s['is_free'])
        }

        # Log to verify data looks correct
        logger.debug(f"Quantum systems data: {json.dumps(result)}")

        return result

    except Exception as e:
        logger.error(f"Error retrieving quantum systems: {e}", exc_info=True)
        # Fallback to hardcoded response if database query fails
        fallback_data = {
            "systems": [
                {
                    "name": "9q-square-qvm",
                    "qubits": 9,
                    "type": "QVM",
                    "is_free": True,
                    "requires_api_key": False,
                    "description": "A 9-qubit quantum virtual machine in a square topology."
                },
                {
                    "name": "9q-square-noisy-qvm",
                    "qubits": 9,
                    "type": "Noisy QVM",
                    "is_free": True,
                    "requires_api_key": False,
                    "description": "A 9-qubit noisy quantum virtual machine in a square topology."
                },
                {
                    "name": "Ankaa-3",
                    "qubits": 84,
                    "type": "QPU",
                    "is_free": False,
                    "requires_api_key": True,
                    "description": "Rigetti Ankaa-3 quantum processing unit."
                }
            ],
            "total_count": 3,
            "free_systems_count": 2,
            "paid_systems_count": 1
        }
        logger.warning(f"Using fallback data for quantum systems: {json.dumps(fallback_data)}")
        return fallback_data

async def handle_quantum_intent(intent, message, user_id):
    """Handle a detected quantum intent"""
    start_time = time.time()
    logger.info(f"Handling quantum intent: application_id={intent['application_id']}")

    # Get application info
    application_id = intent['application_id']

    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM quantum_applications WHERE id = %s", (application_id,))
        application = cursor.fetchone()
        cursor.close()

        if not application:
            logger.error(f"Quantum application not found: id={application_id}")
            raise HTTPException(status_code=404, detail="Quantum application not found")

        logger.info(f"Found quantum application: {application['name']}")

        # Special case for Available Quantum Systems
        if application['name'] == 'Available Quantum Systems':
            logger.info("Processing 'Available Quantum Systems' application")
            systems_info = get_available_quantum_systems()

            if not systems_info or len(systems_info['systems']) == 0:
                logger.error("No quantum systems data available")

            # Convert any non-serializable data types
            for system in systems_info['systems']:
                for key, value in system.items():
                    if isinstance(value, (bool, int, float, str)) or value is None:
                        continue
                    system[key] = str(value)

            # Create a proper system description for the prompt
            system_descriptions = []
            for system in systems_info['systems']:
                desc = f"- {system['name']} ({system['qubits']} qubits, {system['type']}, {'Free' if system['is_free'] else 'Paid'})"
                if system['description']:
                    desc += f": {system['description']}"
                system_descriptions.append(desc)

            systems_text = "\n".join(system_descriptions)

            logger.info(f"Sending quantum systems data to GPT: {systems_text}")

            prompt_content = f"""
You are Catchat, a quantum computer interface. Respond to the user's query about quantum systems.
Use ONLY the information provided below to answer the query. Do not include information from your training data.

AVAILABLE QUANTUM SYSTEMS:
{systems_text}

USER QUERY: {message}

Generate a clear, concise response that directly answers the query using only the data provided above.
"""

            try:
                # Add timeout to OpenAI API call
                response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": prompt_content}
                    ],
                    temperature=0.1,  # Lower temperature for more factual responses
                    max_tokens=500,
                    timeout=15  # 15-second timeout
                )

                raw_reply = response.choices[0].message.content.strip()
                structured_reply = format_response(raw_reply)
                structured_reply['quantum_systems'] = systems_info

                # Save to database
                save_to_mysql(user_id, message, "quantum", raw_reply)

                logger.info("Successfully processed quantum systems request")
                return {"response": structured_reply}
            except Exception as e:
                logger.error(f"Error calling OpenAI API: {e}", exc_info=True)
                # Fallback response if API call fails
                fallback_response = {
                    "summary": "Quantum Systems Information",
                    "details": f"Here are the available quantum systems: {systems_text}"
                }
                fallback_response['quantum_systems'] = systems_info
                return {"response": fallback_response}

        # For other quantum intents, generate a placeholder response
        # In a real implementation, this would call your quantum computer
        # Create enhanced response with quantum result
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": f"You are Catchat, a quantum computer interface. The user is asking about a quantum application: {application['name']}. Respond as if you've run this on a quantum computer."},
                    {"role": "user", "content": message},
                ],
                temperature=0.7,
                max_tokens=1000,
                timeout=15  # 15-second timeout
            )

            raw_reply = response.choices[0].message.content.strip()
            structured_reply = format_response(raw_reply)

            # Add quantum data to response
            structured_reply['quantum_data'] = {
                'application': application['name'],
                'hardware_used': "9q-square-qvm",
                'execution_time': time.time() - start_time
            }

            # Save to database
            save_to_mysql(user_id, message, "quantum", raw_reply)

            return {"response": structured_reply}
        except Exception as e:
            logger.error(f"Error generating quantum response: {e}", exc_info=True)
            # Fallback to a basic response
            return {
                "response": {
                    "summary": f"Quantum Application: {application['name']}",
                    "details": f"I encountered an issue while processing your quantum request. Please try again later."
                }
            }

    except Exception as e:
        logger.error(f"Error handling quantum intent: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to Catchat!"}

@app.get("/test-db")
def test_db():
    """Test endpoint to verify database saving works"""
    try:
        valid_user_id = get_valid_user_id(1)
        if not valid_user_id:
            return {"success": False, "message": "No valid user found in database"}

        conn = get_mysql_connection()
        if conn:
            cursor = conn.cursor()

            # Test insert using a valid user_id
            query = "INSERT INTO chat_history (user_id, message, response) VALUES (%s, %s, %s)"
            cursor.execute(query, (valid_user_id, "Test message from API", "Test response"))

            # Commit the transaction
            conn.commit()
            cursor.close()
            return {"success": True, "message": f"Test data inserted successfully with user ID {valid_user_id}"}
        else:
            return {"success": False, "message": "Could not establish database connection"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/chat/{user_input}")
async def chat_get(user_input: str):
    start_time = time.time()
    logger.info(f"GET /chat/{user_input}")

    try:
        # Detect quantum intent first
        intent = detect_quantum_intent(user_input)

        if intent:
            logger.info(f"Quantum intent detected, forwarding to handler")
            return await handle_quantum_intent(intent, user_input, 1)

        # Standard response if no quantum intent detected
        logger.info(f"No quantum intent detected, using standard GPT response")
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are the user interface to various Quantum Computers. You are also an helpful assistant"},
                    {"role": "user", "content": user_input},
                ],
                temperature=0.7,
                max_tokens=1000,
                timeout=15  # 15-second timeout
            )
            raw_reply = response.choices[0].message.content.strip()
            structured_reply = format_response(raw_reply)

            # Save to database
            save_to_mysql(1, user_input, "standard", raw_reply)

            exec_time = time.time() - start_time
            logger.info(f"Request completed in {exec_time:.2f} seconds")

            return {"response": structured_reply}
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}", exc_info=True)
            # Fallback response if API call fails
            fallback_response = {
                "summary": "Response Unavailable",
                "details": "I'm currently experiencing difficulties processing your request. Please try again in a moment."
            }
            return {"response": fallback_response}
    except Exception as e:
        logger.error(f"Error in chat_get: {e}", exc_info=True)
        exec_time = time.time() - start_time
        logger.info(f"Request failed in {exec_time:.2f} seconds")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/speech-to-text")
async def speech_to_text(file: UploadFile = File(...)):
    """
    Convert audio to text using OpenAI's Whisper model.
    """
    try:
        # Create a temporary file to store the uploaded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_file:
            # Write the uploaded file content to the temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file_name = temp_file.name

        try:
            # Transcribe audio using OpenAI's Whisper model
            with open(temp_file_name, "rb") as audio_file:
                transcript = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            
            # Return the transcribed text
            return {"text": transcript.text}
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_name)
            
    except Exception as e:
        logging.error(f"Error in speech-to-text endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-speech")
async def text_to_speech(request: Request):
    """
    Convert text to speech using OpenAI's TTS model.
    """
    try:
        data = await request.json()
        text = data.get("text")
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        # Select voice based on quantum mode if provided
        voice = data.get("voice", "onyx")
        # Allowed voices: alloy, echo, fable, onyx, nova, shimmer
        
        # Generate speech using OpenAI's TTS model
        response = openai.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        # Return the audio content as a streaming response
        def iterfile():
            yield response.content

        return StreamingResponse(
            iterfile(),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=speech.mp3"}
        )
        
    except Exception as e:
        logging.error(f"Error in text-to-speech endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_post(request_data: ChatRequest, request: Request):
    start_time = time.time()
    logger.info(f"POST /chat with message: {request_data.message[:50]}...")

    user_input = request_data.message
    user_id = get_valid_user_id(request_data.user_id or "1")

    # Get client IP address from request
    client_ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    if not client_ip:
        client_ip = request.client.host
    logger.debug(f"Client IP: {client_ip}")

    # FIRST: check for weather-related query
    weather_keywords = ["weather", "temperature", "forecast", "rain", "snow", "sunny", "cloudy"]
    is_weather_query = any(keyword in user_input.lower() for keyword in weather_keywords)

    if is_weather_query:
        logger.info("Weather-related query detected")

        # Extract location
        location = None
        location_patterns = [
            r"weather (?:in|for|at) (.+?)(?:\?|$|\s+on)",
            r"(?:what's|what is) the weather (?:in|at|for) (.+?)(?:\?|$)",
            r"forecast (?:in|for|at) (.+?)(?:\?|$)",
            r"temperature (?:in|for|at) (.+?)(?:\?|$)",
        ]
        for pattern in location_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                break

        # Check for general weather queries without a location
        general_weather_patterns = [
            # Original patterns
            r"^(?:what'?s|what is|how'?s|how is) the weather(?: like)?(?:\s+today|\s+now)?\??$",
            r"^weather report\??$",
            r"^current weather\??$",
            r"^(?:what'?s|what is) (?:it|the weather) like outside\??$",

            # Single word queries
            r"^weather\??$",
            r"^forecast\??$",
            r"^temperature\??$",

            # Simple queries
            r"^(?:how'?s|how is) it outside\??$",
            r"^(?:what'?s|what is) it like outside\??$",
            r"^(?:how'?s|how is) the sky(?: today| now)?\??$",
            r"^(?:what'?s|what is) the forecast(?: today| now)?\??$",

            # Time-specific queries
            r"^(?:what'?s|what is|how'?s|how is) the weather (?:today|now|right now|currently|at the moment)\??$",
            r"^(?:today'?s|current) weather\??$",
            r"^(?:today'?s|current) forecast\??$",
            r"^weather (?:today|now|right now|currently)\??$",
            r"^temperature (?:today|now|right now|currently)\??$",

            # Weather conditions queries
            r"^is it (?:raining|snowing|sunny|cloudy|windy|cold|hot|warm|chilly)(?: today| now| outside)?\??$",
            r"^(?:will|is) it (?:rain|snow)(?: today| now)?\??$",
            r"^(?:how|do I|should I|will I) (?:cold|hot|warm|windy|rainy) is it(?: today| now| outside)?\??$",
            r"^do I need (?:a coat|an umbrella|jacket|sunglasses)(?: today| now)?\??$",
            r"^should I bring (?:a coat|an umbrella|jacket|sunglasses)(?: today| now)?\??$",

            # Weather-related advice
            r"^what should I wear(?: today| now| outside)?\??$",
            r"^how should I dress(?: today| now| for outside)?\??$",
            r"^should I wear a (?:coat|jacket|sweater|t-shirt)(?: today| now)?\??$",
            r"^will I need (?:a coat|an umbrella|sunscreen)(?: today| now)?\??$",

            # Short conversational queries
            r"^(?:how'?s|how is) it (?:looking|going)(?: outside| today)?\??$",
            r"^(?:nice|good|bad) weather\??$",
            r"^weather update\??$"
        ]
        is_general_query = location is None and any(
            re.search(pattern, user_input, re.IGNORECASE) for pattern in general_weather_patterns
        )

        # If no specific location but a general weather query, get location from IP
        if is_general_query:
            try:
                logger.info(f"General weather query detected. Getting location from IP: {client_ip}")
                location = get_location_from_ip(client_ip)
                if location:
                    logger.info(f"Detected location from IP: {location}")
                else:
                    logger.warning(f"Could not determine location from IP: {client_ip}")
            except Exception as e:
                logger.error(f"Error getting location from IP: {e}", exc_info=True)

        if location:
            logger.info(f"Using location for weather: {location}")

        try:
            # Get weather data
            weather_data = weather_client.get_current_weather(location)
            logger.debug(f"Weather data received: {weather_data is not None}")

            if weather_data:
                # Convert to US units
                us_weather = convert_to_us_units(weather_data)

                # Generate response with weather data in US units using dedented multi-line string
                from textwrap import dedent
                weather_prompt = dedent(f"""
                    You are Catchat, an AI assistant that can provide weather information.
                    Respond to the user's query about weather using ONLY the information provided below.

                    WEATHER DATA FOR {us_weather['location']}:
                    - Temperature: {us_weather['temperature_f']}°F (feels like {us_weather['feels_like_f']}°F)
                    - Conditions: {us_weather['conditions']}
                    - Humidity: {us_weather['humidity']}%
                    - Wind: {us_weather['wind_speed_mph']} mph
                    - Current time there: {us_weather['timestamp']} ({us_weather['timezone']})

                    USER QUERY: {user_input}

                    If this was a general weather query without a specific location, mention that you detected their approximate location based on their IP address.
                    Provide a helpful, conversational response using ONLY the weather data above.
                    Use US standard units (Fahrenheit, mph) in your response.
                """)

                try:
                    response = client.chat.completions.create(
                        model="gpt-4-turbo",
                        messages=[
                            {"role": "system", "content": weather_prompt}
                        ],
                        temperature=0.5,
                        max_tokens=300,
                        timeout=15
                    )

                    raw_reply = response.choices[0].message.content.strip()
                    structured_reply = format_response(raw_reply)

                    # Add weather data to the response
                    structured_reply['weather_data'] = weather_data

                    # Save to database
                    save_to_mysql(
                        user_id=user_id,
                        message=user_input,
                        mode="weather",
                        response=raw_reply
                    )

                    exec_time = time.time() - start_time
                    logger.info(f"Weather request completed in {exec_time:.2f} seconds")

                    return {"response": structured_reply}
                except Exception as e:
                    logger.error(f"Error calling OpenAI API for weather: {e}", exc_info=True)
                    # Continue to normal processing if weather API call fails

        except Exception as e:
            logger.error(f"Error getting weather data: {e}", exc_info=True)
            # Continue to normal processing if weather service fails

    # SECOND, check for quantum intent if weather check didn't return a response
    logger.debug("Checking for quantum intent")
    intent = detect_quantum_intent(user_input)

    if intent:
        logger.info("Quantum intent detected, forwarding to handler")
        return await handle_quantum_intent(intent, user_input, user_id)

    # Standard chat response for non-weather, non-quantum intents
    logger.info("No specific intent detected, using standard GPT response")
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are the user interface to various Quantum Computers. You are also an helpful assistant"},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
            max_tokens=1000,
            timeout=15  # 15-second timeout
        )
        raw_reply = response.choices[0].message.content.strip()
        structured_reply = format_response(raw_reply)

        # Save to database
        save_to_mysql(
            user_id=user_id,
            message=user_input,
            mode=request_data.mode,
            response=raw_reply
        )

        exec_time = time.time() - start_time
        logger.info(f"Request completed in {exec_time:.2f} seconds")

        return {"response": structured_reply}
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}", exc_info=True)

        # Fallback response if API call fails
        fallback_response = {
            "summary": "Response Unavailable",
            "details": "I'm currently experiencing difficulties processing your request. Please try again in a moment."
        }

        exec_time = time.time() - start_time
        logger.info(f"Request failed in {exec_time:.2f} seconds")

        return {"response": fallback_response}

@app.post("/v1/chat/completions")
async def chat_completions(request_data: ChatCompletionRequest):
    # Implementation omitted for brevity
    pass

@app.get("/debug-version")
async def debug_version():
    """Debug endpoint to check if code is reloading"""
    return {
        "version": "1.0.2",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "mysql_connected": mysql_conn is not None and mysql_conn.is_connected()
    }

@app.get("/test-quantum-systems")
async def test_quantum_systems():
    """Test endpoint to directly check quantum systems data"""
    start_time = time.time()
    try:
        systems = get_available_quantum_systems()
        exec_time = time.time() - start_time
        logger.info(f"test-quantum-systems completed in {exec_time:.2f} seconds")

        return {
            "success": True,
            "data": systems,
            "count": systems["total_count"] if systems else 0,
            "execution_time": exec_time
        }
    except Exception as e:
        logger.error(f"Error in test-quantum-systems endpoint: {e}", exc_info=True)
        exec_time = time.time() - start_time
        return {
            "success": False,
            "error": str(e),
            "execution_time": exec_time
        }

@app.get("/api/weather/current/{location}")
async def api_current_weather(location: str):
    """API endpoint for current weather"""
    result = weather_client.get_current_weather(location)
    if not result:
        raise HTTPException(status_code=404, detail=f"Weather data not found for {location}")
    return result

@app.get("/api/weather/forecast/{location}")
async def api_weather_forecast(location: str, days: int = 3):
    """API endpoint for weather forecast"""
    result = weather_client.get_forecast(location, days)
    if not result:
        raise HTTPException(status_code=404, detail=f"Forecast data not found for {location}")
    return result

@app.get("/api/weather/historical/{location}/{date}")
async def api_historical_weather(location: str, date: str):
    """API endpoint for historical weather"""
    result = weather_client.get_historical_weather(location, date)
    if not result:
        raise HTTPException(status_code=404, detail=f"Historical weather data not found for {location} on {date}")
    return result

@app.get("/api/weather/search")
async def api_search_weather(query: str, type: str = "current"):
    """API endpoint for weather search"""
    result = weather_client.search_weather(query, type)
    if not result:
        raise HTTPException(status_code=404, detail=f"Weather data not found for query: {query}")
    return result

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server in development mode")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
