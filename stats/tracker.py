"""Real-time statistics tracker for Valorant"""

import logging
from typing import Dict, Any
from datetime import datetime
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class StatsTracker:
    """Tracks in-game and session statistics"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.current_stats = self._get_empty_stats()
        self.session_history = []
        self.session_start_time = datetime.now()
        
        self.stats_dir = Path(__file__).parent.parent / "stats_data"
        self.stats_dir.mkdir(exist_ok=True)
        
        logger.info("Stats tracker initialized")
    
    def update(self, new_stats: Dict[str, Any]) -> None:
        try:
            previous_stats = self.current_stats.copy()
            self.current_stats.update(new_stats)
            self._detect_stat_changes(previous_stats, self.current_stats)
        except Exception as e:
            logger.error(f"Error updating stats: {e}")
    
    def get_current_stats(self) -> Dict[str, Any]:
        return self.current_stats.copy()
    
    def get_session_stats(self) -> Dict[str, Any]:
        return {
            "session_start": self.session_start_time.isoformat(),
            "session_duration": (datetime.now() - self.session_start_time).total_seconds(),
            "total_kills": self.current_stats.get("kills", 0),
            "total_deaths": self.current_stats.get("deaths", 0),
            "total_assists": self.current_stats.get("assists", 0),
            "total_score": self.current_stats.get("score", 0),
            "matches_played": len(self.session_history),
        }
    
    def save_session(self) -> bool:
        try:
            filename = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = self.stats_dir / filename
            
            session_data = {
                "session_stats": self.get_session_stats(),
                "current_stats": self.current_stats,
                "history": self.session_history
            }
            
            with open(filepath, 'w') as f:
                json.dump(session_data, f, indent=2, default=str)
            
            logger.info(f"Session saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving session: {e}")
            return False
    
    def _detect_stat_changes(self, old_stats: Dict[str, Any], new_stats: Dict[str, Any]) -> None:
        try:
            if new_stats.get("kills", 0) > old_stats.get("kills", 0):
                logger.debug("Kill detected!")
            
            if new_stats.get("deaths", 0) > old_stats.get("deaths", 0):
                logger.debug("Death detected!")
        except Exception as e:
            logger.debug(f"Error detecting stat changes: {e}")
    
    def _get_empty_stats(self) -> Dict[str, Any]:
        return {
            "kills": 0,
            "deaths": 0,
            "assists": 0,
            "score": 0,
            "agent": "Unknown",
            "economy": 0,
            "headshot_percent": 0.0,
            "round": 0,
            "is_in_game": False,
        }