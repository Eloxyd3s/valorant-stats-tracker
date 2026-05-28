"""Valorant API client for communicating with game client"""

import requests
import logging
from typing import Dict, Any, Optional
import psutil

logger = logging.getLogger(__name__)


class ValorantAPIClient:
    """Client for interfacing with Valorant's local API"""
    
    VALORANT_PROCESS_NAME = "VALORANT.exe"
    DEFAULT_API_PORT = 3000
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        valorant_config = config.get("valorant", {})
        self.api_port = valorant_config.get("api_port", self.DEFAULT_API_PORT)
        self.api_timeout = valorant_config.get("api_timeout", 5000) / 1000
        
        self.base_url = f"http://127.0.0.1:{self.api_port}"
        self.session = requests.Session()
        self.session.verify = False
        
        self.current_stats = {}
        self.connected = False
        
        logger.info(f"Valorant API client initialized on port {self.api_port}")
    
    def update(self) -> bool:
        try:
            if not self._is_valorant_running():
                self.connected = False
                return False
            
            stats_data = self._fetch_player_stats()
            if stats_data:
                self.current_stats = stats_data
                self.connected = True
                return True
            
            return False
        except Exception as e:
            logger.debug(f"Error updating stats: {e}")
            self.connected = False
            return False
    
    def get_current_stats(self) -> Dict[str, Any]:
        return self.current_stats if self.connected else self._get_default_stats()
    
    def _is_valorant_running(self) -> bool:
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == self.VALORANT_PROCESS_NAME:
                    return True
            return False
        except Exception as e:
            logger.debug(f"Error checking Valorant process: {e}")
            return False
    
    def _fetch_player_stats(self) -> Optional[Dict[str, Any]]:
        try:
            endpoint = f"{self.base_url}/player/stats"
            response = self.session.get(endpoint, timeout=self.api_timeout)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.debug(f"API returned status code {response.status_code}")
                return None
        except requests.exceptions.Timeout:
            logger.debug("API request timeout")
            return None
        except requests.exceptions.ConnectionError:
            logger.debug("Could not connect to Valorant API")
            return None
        except Exception as e:
            logger.debug(f"Error fetching player stats: {e}")
            return None
    
    def _get_default_stats(self) -> Dict[str, Any]:
        return {
            "kills": 0,
            "deaths": 0,
            "assists": 0,
            "score": 0,
            "agent": "Unknown",
            "economy": 0,
            "headshot_percent": 0.0,
            "is_in_game": False,
            "round": 0,
            "team_color": None
        }