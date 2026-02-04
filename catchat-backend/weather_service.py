import os
import requests
import logging
from datetime import datetime, timedelta
from functools import lru_cache

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/root/catchat-backend/backend.log',
    filemode='a'
)
logger = logging.getLogger("weather_service")

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("VISUAL_CROSSING_API_KEY")
        if not self.api_key:
            logger.error("VISUAL_CROSSING_API_KEY not found in environment variables")
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

    def get_current_weather(self, location):
        """Get current weather conditions for a location"""
        try:
            url = f"{self.base_url}/{location}/today"
            params = {
                "unitGroup": "metric",
                "include": "current",  # Request current data
                "key": self.api_key,
                "contentType": "json"
            }

            logger.debug(f"Fetching current weather for {location} from URL: {url} with params: {params}")
            response = requests.get(url, params=params, timeout=10)
            logger.debug(f"Response status code: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Response JSON: {data}")

            # If "currentConditions" is missing, fallback to the first element of "days"
            if not data.get('currentConditions'):
                if data.get('days') and len(data['days']) > 0:
                    logger.warning(f"'currentConditions' not found for {location}; using first day from 'days' as current weather")
                    current = data['days'][0]
                else:
                    logger.warning(f"No weather data found for {location}")
                    return None
            else:
                current = data['currentConditions']

            result = {
                'location': data.get('resolvedAddress', location),
                'temperature': current.get('temp'),
                'feels_like': current.get('feelslike'),
                'humidity': current.get('humidity'),
                'wind_speed': current.get('windspeed'),
                'wind_direction': current.get('winddir'),
                'conditions': current.get('conditions'),
                'description': self._get_weather_description(current),
                'icon': current.get('icon'),
                'timestamp': current.get('datetime'),
                'timezone': data.get('timezone')
            }

            logger.debug(f"Successfully retrieved current weather for {location}: {result}")
            return result
        except Exception as e:
            logger.error(f"Error fetching current weather: {e}", exc_info=True)
            return None

    def get_forecast(self, location, days=3):
        """Get weather forecast for a location"""
        try:
            url = f"{self.base_url}/{location}/next{days}days"
            params = {
                "unitGroup": "metric",
                "include": "days",
                "key": self.api_key,
                "contentType": "json"
            }

            logger.debug(f"Fetching {days}-day forecast for {location} from URL: {url} with params: {params}")
            response = requests.get(url, params=params, timeout=10)
            logger.debug(f"Response status code: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Response JSON: {data}")

            if not data.get('days'):
                logger.warning(f"No forecast data found for {location}")
                return None

            forecasts = []
            for day in data['days'][:days]:
                forecast = {
                    'date': day.get('datetime'),
                    'temp_max': day.get('tempmax'),
                    'temp_min': day.get('tempmin'),
                    'conditions': day.get('conditions'),
                    'description': self._get_weather_description(day),
                    'icon': day.get('icon'),
                    'precipitation_probability': day.get('precipprob')
                }
                forecasts.append(forecast)

            result = {
                'location': data.get('resolvedAddress', location),
                'forecasts': forecasts,
                'timezone': data.get('timezone')
            }

            logger.debug(f"Successfully retrieved forecast for {location}: {result}")
            return result
        except Exception as e:
            logger.error(f"Error fetching forecast: {e}", exc_info=True)
            return None

    @lru_cache(maxsize=16)
    def get_historical_weather(self, location, date):
        """Get historical weather for a specific date"""
        try:
            url = f"{self.base_url}/{location}/{date}"
            params = {
                "unitGroup": "metric",
                "include": "days",
                "key": self.api_key,
                "contentType": "json"
            }

            logger.debug(f"Fetching historical weather for {location} on {date} from URL: {url} with params: {params}")
            response = requests.get(url, params=params, timeout=10)
            logger.debug(f"Response status code: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Response JSON: {data}")

            if not data.get('days'):
                logger.warning(f"No historical data found for {location} on {date}")
                return None

            day = data['days'][0]
            result = {
                'location': data.get('resolvedAddress', location),
                'date': day.get('datetime'),
                'temp_max': day.get('tempmax'),
                'temp_min': day.get('tempmin'),
                'temp_avg': day.get('temp'),
                'humidity': day.get('humidity'),
                'conditions': day.get('conditions'),
                'description': self._get_weather_description(day),
                'precipitation': day.get('precip'),
                'wind_speed': day.get('windspeed')
            }

            logger.debug(f"Successfully retrieved historical data for {location} on {date}: {result}")
            return result
        except Exception as e:
            logger.error(f"Error fetching historical weather: {e}", exc_info=True)
            return None

    def _get_weather_description(self, data):
        """Generate a human-readable weather description"""
        conditions = data.get('conditions', 'No conditions available')
        temp = data.get('temp')
        humidity = data.get('humidity')
        wind_speed = data.get('windspeed')

        description = f"{conditions}"
        if temp is not None:
            description += f", temperature {temp}°C"
        if humidity is not None:
            description += f", humidity {humidity}%"
        if wind_speed is not None:
            description += f", wind speed {wind_speed} km/h"

        return description

