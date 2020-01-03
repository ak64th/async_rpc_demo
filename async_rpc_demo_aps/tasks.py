import time


def detect_type_1(infrared_image, visible_image):
    time.sleep(1)
    return {'file': 'path/of/result.npy'}


def detect_type_2(infrared_image, visible_image):
    # raise an exception
    return {'num': 1 / 0}
