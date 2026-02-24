from src.vision_pipeline import process_document

def process_multiple_documents(image_paths):
    """
    Process multiple document images independently.
    """
    results = []

    for path in image_paths:
        result = process_document(path)
        result["source_image"] = path
        results.append(result)

    return results
