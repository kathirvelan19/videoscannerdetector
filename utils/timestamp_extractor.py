import cv2

def get_timestamp(cap):

    ms = cap.get(cv2.CAP_PROP_POS_MSEC)

    seconds = ms / 1000

    minutes = int(seconds // 60)
    sec = int(seconds % 60)

    return f"{minutes:02}:{sec:02}"