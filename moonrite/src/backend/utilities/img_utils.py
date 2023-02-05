import cv2 as cv
import numpy as np


def template_search(window_stream, template, threshold):
    window_stream.update_frame()
    frame = window_stream.get_region('screen')
    method = cv.TM_CCOEFF_NORMED
    res = cv.matchTemplate(frame, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    if max_val > threshold:
        return max_loc
    else:
        return None


def template_search_global(frame, template, threshold):
    method = cv.TM_CCOEFF_NORMED
    res = cv.matchTemplate(frame, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    if max_val > threshold:
        return max_loc
    else:
        return None


def img_center(loc, image):
    x, y = loc
    return (x + image.shape[1]//2, y + image.shape[0]//2)


def show_img(name, img):
    cv.namedWindow(name, cv.WINDOW_NORMAL)
    cv.imshow(name, img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def show_img_no_wait(name, img):
    cv.namedWindow(name, cv.WINDOW_NORMAL)
    cv.imshow(name, img)


def show_imgs(names, imgs):
    for ind, name in enumerate(names):
        cv.namedWindow(name, cv.WINDOW_NORMAL)
        cv.imshow(name, imgs[ind])
    cv.waitKey(0)
    cv.destroyAllWindows()


def scale_img(img, scale_percent):
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    dim = (width, height)
    return cv.resize(img, dim, interpolation=cv.INTER_AREA)


def dilate_img(img, dilation_size):
    kernel = np.ones((dilation_size, dilation_size), np.uint8)
    dilated_img = cv.dilate(img, kernel)
    return dilated_img
