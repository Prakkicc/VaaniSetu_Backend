import cv2
import numpy as np

def detect_blur(image):
    """
    Detect blur level using variance of Laplacian.
    Returns: SHARP, MILD_BLUR, or HEAVY_BLUR
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    # print("Blur score:", laplacian_var)

    # Thresholds (can tune later)
    if laplacian_var > 80:
        return "SHARP"
    elif laplacian_var > 30:
        return "MILD_BLUR"
    else:
        return "HEAVY_BLUR"