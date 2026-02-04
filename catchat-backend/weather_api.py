from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import os
import logging
from dotenv import load_dotenv
from weather_service import WeatherService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/root/catchat-backend/weather.log',
    filemode='a'
)
logger = logging.getLogger("weather_api")

# Initialize FastAPI app
app = FastAPI(title="Weather API")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.qcatchat.com", "https://qcatchat.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
)

# Initialize the weather service
weather_service = WeatherService()

@app.get("/")
async def home():
    return {"message": "Welcome to the Weather API"}

@app.get("/weather/current/{location}")
async def get_current_weather(location: str):
    """Get current weather for a location"""
    logger.info(f"Current weather request for {location}")
    try:
        result = weather_service.get_current_weather(location)
        if not result:
            logger.warning(f"No weather data found for {location}")
            raise HTTPException(status_code=404, detail=f"Weather data not found for {location}")
        
        return result
    except Exception as e:
        logger.error(f"Error in current weather endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/forecast/{location}")
async def get_weather_forecast(location: str, days: int = 3):
    """Get weather forecast for a location"""
    logger.info(f"Forecast request for {location}, {days} days")
    try:
        if days < 1 or days > 15:
            raise HTTPException(status_code=400, detail="Days parameter must be between 1 and 15")
            
        result = weather_service.get_forecast(location, days)
        if not result:
            logger.warning(f"No forecast data found for {location}")
            raise HTTPException(status_code=404, detail=f"Forecast data not found for {location}")
        
        return result
    except Exception as e:
        logger.error(f"Error in forecast endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/historical/{location}/{date}")
async def get_historical_weather(location: str, date: str):
    """Get historical weather for a location on a specific date"""
    logger.info(f"Historical weather request for {location} on {date}")
    try:
        # Validate date format (YYYY-MM-DD)
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Date must be in YYYY-MM-DD format")
            
        result = weather_service.get_historical_weather(location, date)
        if not result:
            logger.warning(f"No historical data found for {location} on {date}")
            raise HTTPException(status_code=404, detail=f"Historical weather data not found for {location} on {date}")
        
        return result
    except Exception as e:
        logger.error(f"Error in historical weather endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/search")
async def search_weather(query: str, type: str = "current"):
    """Search weather data based on query and type"""
    logger.info(f"Weather search request: {query}, type: {type}")
    try:
        if type not in ["current", "forecast", "historical"]:
            raise HTTPException(status_code=400, detail="Type must be 'current', 'forecast', or 'historical'")
        
        # Extract location and possibly date from query
        location = query
        date = None
        
        # If query contains a date reference for historical data
        if type == "historical":
            # Very simple date extraction - in a real app, you'd use NLP
            if " on " in query:
                location, date_part = query.split(" on ", 1)
                # Try to parse date - very basic implementation
                try:
                    date_obj = datetime.strptime(date_part.strip(), "%Y-%m-%d")
                    date = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    # If can't parse, use a date one week ago
                    date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            else:
                # Default to a week ago
                date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        # Call the appropriate weather service method
        if type == "current":
            result = weather_service.get_current_weather(location)
        elif type == "forecast":
            result = weather_service.get_forecast(location)
        else:  # historical
            result = weather_service.get_historical_weather(location, date)
        
        if not result:
            logger.warning(f"No weather data found for query: {query}")
            raise HTTPException(status_code=404, detail=f"Weather data not found for query: {query}")
        
        return {
            "query": query,
            "type": type,
            "result": result
        }
    except Exception as e:
        logger.error(f"Error in weather search endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "weather-api",
        "api_key_configured": bool(os.getenv("VISUAL_CROSSING_API_KEY"))
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Weather API server")
    uvicorn.run("weather_api:app", host="0.0.0.0", port=8001, reload=True)
