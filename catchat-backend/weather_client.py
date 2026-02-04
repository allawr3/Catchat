import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("catchat")

class WeatherClient:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
    
    def get_current_weather(self, location: str) -> Optional[Dict[str, Any]]:
        """Get current weather for a location"""
        try:
            url = f"{self.base_url}/weather/current/{location}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error getting current weather: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Exception in weather client: {e}")
            return None
    
    def get_forecast(self, location: str, days: int = 3) -> Optional[Dict[str, Any]]:
        """Get weather forecast for a location"""
        try:
            url = f"{self.base_url}/weather/forecast/{location}"
            params = {"days": days}
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error getting forecast: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Exception in weather client: {e}")
            return None
    
    def get_historical_weather(self, location: str, date: str) -> Optional[Dict[str, Any]]:
        """Get historical weather for a location on a specific date"""
        try:
            url = f"{self.base_url}/weather/historical/{location}/{date}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error getting historical weather: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Exception in weather client: {e}")
            return None
    
    def search_weather(self, query: str, type: str = "current") -> Optional[Dict[str, Any]]:
        """Search weather data based on query and type"""
        try:
            url = f"{self.base_url}/weather/search"
            params = {"query": query, "type": type}
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error searching weather: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Exception in weather client: {e}")
            return None
