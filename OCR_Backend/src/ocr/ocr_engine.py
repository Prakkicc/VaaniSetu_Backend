from paddleocr import PaddleOCR

# Initialize OCR once (angle classification is enabled here, which is correct)
ocr = PaddleOCR(use_angle_cls=True, lang='en')

def run_ocr(image_path: str) -> str:
    """
    Runs OCR on an image and returns extracted text as a single string.
    """
    # FIX: Removed cls=True as it is not supported in this function call
    result = ocr.ocr(image_path)

    # FIX: Safety check in case the OCR finds no text at all
    if not result or not result[0]:
        return ""

    lines = []

    for line in result[0]:
        text = line[1][0]
        lines.append(text)

    return "\n".join(lines)