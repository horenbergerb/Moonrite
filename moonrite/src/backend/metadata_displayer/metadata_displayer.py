import numpy as np
import cv2 as cv

class MetadataDisplayer:
    def __init__(self, config):
        self.config = config

    def plot_feature_matches_(self, img1, img2, kp1, kp2, good_matches):

        img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype=np.uint8)
        cv.drawMatches(img1, kp1, img2, kp2,
                    good_matches, img_matches, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv.namedWindow('Good Feature Matches', cv.WINDOW_NORMAL)
        cv.imshow('Good Feature Matches', img_matches)
        k = cv.waitKey(1)
        if k == ord('q'):
            cv.destroyWindow('Good Feature Matches')
            return False
        else:
            return True

    def run(self, frame, metadata):
        running = self.plot_feature_matches_(metadata['compass']['compass'],
                                             metadata['compass']['compass_north'],
                                             metadata['compass']['compass_kp'],
                                             metadata['compass']['compass_north_kp'],
                                             metadata['compass']['good_matches'])
        return running