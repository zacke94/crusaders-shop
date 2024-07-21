import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import date

def _file_name():
    today = date.today()
    return f"logs/{today.strftime('%b_%d_%Y')}.log"

class Logger:
    _instance = None  # Class-level variable to store singleton instance

    def __new__(cls, log_file='app.log', log_level=logging.DEBUG, max_bytes=5000000, backup_count=5):
        """Ensures only one instance of Logger is created (singleton)."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(log_file, log_level, max_bytes, backup_count)
        return cls._instance

    def _initialize(self, log_file, log_level, max_bytes, backup_count):
        """Initializes the logger instance (called only once)."""
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(log_level)

        # Formatter for logs
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # File handler with rotation
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self._create_directory_if_not_exists('logs')

    def _create_directory_if_not_exists(self, directory):
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Directory '{directory}' is ready.")
        except Exception as e:
            print(f"Error creating directory '{directory}': {e}")

    def debug(self, message):
        """Logs a debug message."""
        self.logger.debug(message)

    def info(self, message):
        """Logs an info message."""
        self.logger.info(message)

    def warning(self, message):
        """Logs a warning message."""
        self.logger.warning(message)

    def error(self, message):
        """Logs an error message."""
        self.logger.error(message)

    def critical(self, message):
        """Logs a critical message."""
        self.logger.critical(message)


# Create a global instance that can be imported and used in any module

logger_instance = Logger(log_file=_file_name(), log_level=logging.DEBUG)