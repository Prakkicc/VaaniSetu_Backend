import cv2
import numpy as np

def enhance_image(image):
    """
    Light enhancement for mildly blurred images.
    """

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase contrast using histogram equalization
    contrast = cv2.equalizeHist(gray)

    # Light sharpening kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])

    sharpened = cv2.filter2D(contrast, -1, kernel)

    return sharpened
