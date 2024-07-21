import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler

class Logger:
    _instance = None  # Class-level variable to store singleton instance

    def __new__(cls, log_level=logging.DEBUG, max_bytes=5000000, backup_count=5):
        """Ensures only one instance of Logger is created (singleton)."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(log_level, max_bytes, backup_count)
        return cls._instance

    def _initialize(self, log_level, max_bytes, backup_count):
        self._create_directory_if_not_exists('logs')

        """Initializes the logger instance (called only once)."""
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(log_level)

        # Formatter for logs
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # File handler with rotation
        file_handler = RotatingFileHandler('logs/application.log', maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self._start_log_scheduler()

    def _extract_todays_logs(self):
        try:
            log_file_path = 'logs/application.log'  # Replace with actual log file path
            new_log_file_path = f'logs/{date.today().strftime("%b_%d_%Y")}.log'

            today = date.today().strftime("%Y-%m-%d")

            if os.path.exists(log_file_path):
                with open(log_file_path, 'r') as log_file:
                    logs = log_file.readlines()

                todays_logs = [log for log in logs if today in log]

                with open(new_log_file_path, 'w') as new_log_file:
                    new_log_file.writelines(todays_logs)

                self.info(f"Today's logs have been saved to {new_log_file_path}")
            else:
                self.warning(f"Log file not found at {log_file_path}")
        except Exception as e:
            self.error(f"Failed to create today's log: {e}")

    def _start_log_scheduler(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=self._extract_todays_logs, trigger='cron', hour=22, minute=20)
        scheduler.start()

    def _file_name(self):
        today = date.today()
        return f"logs/{today.strftime('%b_%d_%Y')}.log"

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

logger_instance = Logger(log_level=logging.DEBUG)