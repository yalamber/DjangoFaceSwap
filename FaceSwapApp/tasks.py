from __future__ import absolute_import

from celery import shared_task

import cv2
import base64
import numpy as np

from .align import faceSwapImages


def base64_to_image(imageb64):
    raw = base64.decodestring(imageb64.split(',')[1].replace("data:image/png;",""))
    image = np.frombuffer(raw, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.CV_LOAD_IMAGE_COLOR)
    return image

def image_to_base64(image):
    jpgdata = cv2.imencode('.jpg',image)[1]
    b64 = "data:image/jpg;base64,"+base64.encodestring(jpgdata)
    return b64

@shared_task
def faceSwapTask(imageb64):
    try:
        image = base64_to_image(imageb64)
        swapped = faceSwapImages(image)
        replyb64 = image_to_base64(swapped)

        return replyb64

    except Exception as e:
        #no face to transform
        return None