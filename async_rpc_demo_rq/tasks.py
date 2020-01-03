import time


def detect_type_1(image_url):
    time.sleep(1)
    return {'file': 'path/of/result.npy'}


def detect_type_2(image_url):
    # raise an exception
    return {'num': 1 / 0}


DETECTION_TASK_TYPE_MAPPING = {
    1: detect_type_1,
    2: detect_type_2,
}
