"""Configuration management for the Valorant Stats Tracker"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration"""
    
    DEFAULT_CONFIG_PATH = Path(__file__).parent / "config.json"
    
    def __init__(self, config_path: str = None):
        self.config_path = Path(config_path) if config_path else self.DEFAULT_CONFIG_PATH
        self.config = {}
    
    def load_config(self) -> Dict[str, Any]:
        try:
            if not self.config_path.exists():
                logger.warning(f"Config file not found at {self.config_path}")
                return self._get_default_config()
            
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            
            logger.info(f"Configuration loaded from {self.config_path}")
            return self.config
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def save_config(self, config: Dict[str, Any] = None) -> bool:
        try:
            config_to_save = config if config else self.config
            
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            
            logger.info(f"Configuration saved to {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value: Any) -> bool:
        try:
            keys = key.split('.')
            config = self.config
            
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            config[keys[-1]] = value
            return True
            
        except Exception as e:
            logger.error(f"Error setting config value: {e}")
            return False
    
    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "overlay": {
                "position": {"x": 1700, "y": 50},
                "scale": 1.0,
                "transparency": 0.9,
                "width": 300,
                "height": 400,
                "update_interval": 100,
                "locked": False
            },
            "display": {
                "theme": "dark",
                "font_size": 14,
                "show_graph": True,
                "animation_enabled": True
            },
            "stats": {
                "track_kills": True,
                "track_deaths": True,
                "track_assists": True
            },
            "valorant": {
                "api_port": 3000,
                "api_timeout": 5000
            }
        }
