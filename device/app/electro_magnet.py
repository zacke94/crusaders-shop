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
        self.lock()

    def lock(self):
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.OUT)
        GPIO.output(gpio_pin, GPIO.LOW)"""

    def unlock(self):
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.OUT)
        GPIO.output(gpio_pin, GPIO.HIGH)"""


electro_magnet_instance = ElectroMagnet()

