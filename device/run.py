from app import create_app
from app.logger import logger_instance
from app.electro_magnet import electro_magnet_instance
import argparse

app = create_app()

if __name__ == '__main__':
    try:
        logger_instance.info("App is running.")
        app.run(debug=True)
        electro_magnet_instance.lock()
    finally:
        logger_instance.info("Terminating the app")
        electro_magnet_instance.unlock()
        electro_magnet_instance.cleanup()