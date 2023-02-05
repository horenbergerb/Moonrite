import numpy as np
import pyautogui as pag
from datetime import datetime
import logging

from src.backend.analytics.compass import Compass


class AnalyticsPipeline:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config=config

        self.compass = Compass(self.config)
    
    def run(self, frame, metadata):
        metadata['compass'] = self.compass.update(frame)
        return metadata