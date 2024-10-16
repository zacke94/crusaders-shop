"""import RPi.GPIO as GPIO
"""
from .logger import logger_instance

class ElectroMagnet:
    _instance = None  # Class-level variable to store singleton instance
    _gpio_pin = 23

    def __new__(cls):
        """Ensures only one instance of ElectroMagnet is created (singleton)."""
        if cls._instance is None:
            cls._instance = super(ElectroMagnet, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        try:
            self.lock()
            logger_instance.info("Successfully locked device at startup")
        except Exception as e:
            logger_instance.critical("Could not lock device at startup")

    def lock(self):
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(_gpio_pin, GPIO.OUT)
        GPIO.output(_gpio_pin, GPIO.LOW)"""

    def unlock(self):
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(_gpio_pin, GPIO.OUT)
        GPIO.output(_gpio_pin, GPIO.HIGH)"""


electro_magnet_instance = ElectroMagnet()

