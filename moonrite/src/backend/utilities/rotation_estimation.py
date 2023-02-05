import cv2 as cv
import numpy as np


def get_feature_matches(img1, img2, config):
    # Initiate SIFT detector
    sift = cv.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < config['lowe_ratio_thresh'] * n.distance:
            good_matches.append(m)

    return kp1, des1, kp2, des2, good_matches


def plot_feature_matches(img1, img2, config):
    kp1, des1, kp2, des2, good_matches = get_feature_matches(img1, img2, config)

    img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype=np.uint8)
    cv.drawMatches(img1, kp1, img2, kp2,
                   good_matches, img_matches, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv.namedWindow('Good Feature Matches', cv.WINDOW_NORMAL)
    cv.imshow('Good Feature Matches', img_matches)
    cv.waitKey(0)
    cv.destroyAllWindows()


def estimate_rotation_matrix(img1, img2, config):
    kp1, des1, kp2, des2, good_matches = get_feature_matches(img1, img2, config)

    if len(good_matches) > config['min_match_count']:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        M, mask = cv.estimateAffine2D(src_pts, dst_pts, cv.RANSAC)
        return kp1, M, mask
    return None, None


def rotation_matrix_to_angle(M):
    if M is not None:
        return np.arctan2(-1 * M[0, 1], M[0, 0])
    return None