import logging
import cv2 as cv
import numpy as np

from src.backend.utilities.rotation_estimation import rotation_matrix_to_angle, estimate_rotation_matrix, plot_feature_matches
from src.backend.utilities.img_utils import scale_img


class Compass:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config

        self.sift = cv.SIFT_create()

        # north-facing compass which we will approximate angle relative to
        self.compass_north = cv.imread(self.config['compass']['compass_file'])
        self.prepare_compass_north_()

        self.compass_x1, self.compass_y1, self.compass_x2, self.compass_y2 = self.config['regions']['compass']

        self.compass = None

    def prepare_compass_north_(self):
        self.compass_north = self.preprocess_compass_(self.compass_north)
        self.compass_north_kp, self.compass_north_des = self.sift.detectAndCompute(self.compass_north, None)

    def update(self, frame):
        self.logger.info('Calculating compass metadata')
        self.compass = frame[self.compass_y1:self.compass_y2, self.compass_x1:self.compass_x2]
        return self.calculate_compass_metadata_()

    def preprocess_compass_(self, compass):
        scale_percent = self.config['compass']['rotation_estimation']['compass_scale']
        compass = cv.cvtColor(compass, cv.COLOR_BGR2GRAY)
        compass = scale_img(compass, scale_percent)
        return compass

    def match_features_(self, kp1, des1, kp2, des2):
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)

        good_matches = []
        for m, n in matches:
            if m.distance < self.config['compass']['rotation_estimation']['lowe_ratio_thresh'] * n.distance:
                good_matches.append(m)

        return good_matches
    
    def estimate_rotation_matrix_(self, kp1, kp2, good_matches):
        if len(good_matches) > self.config['compass']['rotation_estimation']['min_match_count']:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            M, mask = cv.estimateAffine2D(src_pts, dst_pts, cv.RANSAC)
            return M, mask
        return None, None

    def calculate_compass_metadata_(self):
        compass = self.preprocess_compass_(self.compass)
        compass_kp, compass_des = self.sift.detectAndCompute(compass, None)

        good_matches = self.match_features_(compass_kp, compass_des, self.compass_north_kp, self.compass_north_des)

        compass_rotation_matrix, mask = self.estimate_rotation_matrix_(compass_kp, self.compass_north_kp, good_matches)
        compass_angle = rotation_matrix_to_angle(compass_rotation_matrix)

        return {'compass': compass,
                'compass_kp': compass_kp,
                'compass_des': compass_des,
                'good_matches': good_matches,
                'compass_rotation_matrix': compass_rotation_matrix,
                'compass_angle': compass_angle,
                'compass_north': self.compass_north,
                'compass_north_kp': self.compass_north_kp,
                'compass_north_des': self.compass_north_des}