#!/usr/bin/env python3
"""Valorant Stats Tracker Overlay - Main Application Entry Point"""

import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('valorant_tracker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from overlay.window import OverlayWindow
from valorant.api_client import ValorantAPIClient
from stats.tracker import StatsTracker
from config_manager import ConfigManager


class ValorantStatsTrackerApp:
    """Main application class"""
    
    def __init__(self):
        """Initialize the Valorant Stats Tracker application"""
        logger.info("Initializing Valorant Stats Tracker...")
        
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        self.api_client = ValorantAPIClient(self.config)
        self.stats_tracker = StatsTracker(self.config)
        self.overlay = None
        
        logger.info("Application initialized successfully")
    
    def start(self):
        """Start the application"""
        try:
            logger.info("Starting Valorant Stats Tracker Overlay...")
            
            self.overlay = OverlayWindow(
                config=self.config,
                api_client=self.api_client,
                stats_tracker=self.stats_tracker
            )
            
            self.overlay.run()
            
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            sys.exit(1)
    
    def shutdown(self):
        """Clean shutdown"""
        logger.info("Shutting down application...")
        if self.overlay:
            self.overlay.stop()
        self.stats_tracker.save_session()
        logger.info("Application closed")


def main():
    """Main entry point"""
    app = ValorantStatsTrackerApp()
    
    try:
        app.start()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    finally:
        app.shutdown()


if __name__ == "__main__":
    main()