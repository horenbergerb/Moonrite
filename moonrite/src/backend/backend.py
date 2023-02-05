from datetime import datetime
import pyautogui as pag
import numpy as np

from src.backend.analytics.analytics import AnalyticsPipeline
from src.backend.metadata_displayer.metadata_displayer import MetadataDisplayer

class Backend:
    def __init__(self, config):
        self.config = config
        self.osrs_x1, self.osrs_y1, self.osrs_x2, self.osrs_y2 = self.config['regions']['osrs']

        self.analytics_pipeline = AnalyticsPipeline(config)
        self.metadata_displayer = MetadataDisplayer(config)

    def capture_screen(self):
        timestamp = datetime.now()
        frame = np.array(pag.screenshot())[self.osrs_y1:self.osrs_y2, self.osrs_x1:self.osrs_x2]
        frame = frame[:, :, ::-1]
        return frame, timestamp

    def run_frame_(self):
        frame, timestamp = self.capture_screen()
        metadata = {'timestamp': timestamp}

        metadata = self.analytics_pipeline.run(frame, metadata)

        running = self.metadata_displayer.run(frame, metadata)

        # TODO: save/broadcast metadata somehow

        return frame, metadata, running
    
    def run(self):
        running = True
        while running:
            _, _, running = self.run_frame_()