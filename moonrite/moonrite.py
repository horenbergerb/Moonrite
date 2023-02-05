from src.backend.backend import Backend
from src.frontend.frontend import Frontend
import yaml
import logging
import signal
import threading
import os

from src.backend.utilities.utilities import launch_runelite


class Moonrite:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, filename="logs/moonrite.log", filemode='w')

        config = yaml.safe_load(open('data/config.yaml'))


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO, filename="data/moonrite.log", filemode='w')

        config = yaml.safe_load(open('data/config.yaml'))

        backend = Backend(config)
        
        runelite_thread = threading.Thread(target=launch_runelite)
        runelite_thread.start()

        backend_thread = threading.Thread(target=backend.run)
        backend_thread.start()

        backend_thread.join()
        runelite_thread.join()

        # gui = MoonriteGui(window_stream, controller, navigator, config)
        # gui.run()

        logging.info('MoonRite execution complete. Exiting...')
    except KeyboardInterrupt:
        logging.info('MoonRite killed by keyboard interrupt')

