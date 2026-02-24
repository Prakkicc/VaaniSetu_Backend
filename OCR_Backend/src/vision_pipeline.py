from paddleocr import PaddleOCR
from src.doc_classifier.detect_doc_type import detect_document_type
from src.extraction.birth_extractor import extract_birth_fields
from src.ocr.ocr_engine import run_ocr



def process_document(image_path: str) -> dict:
    """
    Input: path to certificate image
    Output: dict with document_type and extracted fields
    """
    text = run_ocr(image_path)
    lines = text.split("\n")

    doc_type = detect_document_type(lines)

    output = {
        "document_type": doc_type,
        "fields": {}
    }

    if doc_type == "Birth Certificate":
        output["fields"] = extract_birth_fields(lines)

    print("OCR TEXT:\n", text)


    return output
