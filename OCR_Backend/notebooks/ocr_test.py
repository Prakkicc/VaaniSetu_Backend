from paddleocr import PaddleOCR

from src.doc_classifier.detect_doc_type import detect_document_type
from src.extraction.birth_extractor import extract_birth_fields


def main():
    ocr = PaddleOCR(use_angle_cls=True, lang='en')

    img_path = "data/raw/birth_1.jpg"
    result = ocr.ocr(img_path, cls=True)

    lines = []
    for line in result[0]:
        text = line[1][0]
        lines.append(text)
        print(text)

    doc_type = detect_document_type(lines)
    print("\nDetected Document Type:", doc_type)

    if doc_type == "Birth Certificate":
        fields = extract_birth_fields(lines)
        print("\nExtracted Fields:")
        for k, v in fields.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
