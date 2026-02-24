import os
# THESE MUST BE THE VERY FIRST LINES IN THE FILE!
# This disables the broken PIR engine and oneDNN on Windows
os.environ["FLAGS_enable_pir_api"] = "0"
os.environ["FLAGS_use_mkldnn"] = "0"
os.environ["PADDLE_DISABLE_MKLDNN"] = "1"

from fastapi import FastAPI, UploadFile, File
from typing import List
import shutil

import uuid
import json
from datetime import datetime

from src.multi_document_pipeline import process_multiple_documents
from src.person_merger import merge_documents

app = FastAPI(title="Document AI Service")

UPLOAD_DIR = "data/uploads"
JSON_DIR = "data/json_outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)


@app.post("/process-documents")
async def process_documents(files: List[UploadFile] = File(...)):
    image_paths = []

    # Save uploaded images
    for file in files:
        ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        image_paths.append(filepath)

    # OCR + extraction
    doc_results = process_multiple_documents(image_paths)
    person_profile = merge_documents(doc_results)

    # Build final JSON
    output = {
        "request_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "documents": doc_results,
        "person_profile": person_profile
    }

    # Save JSON to disk
    json_filename = f"{output['request_id']}.json"
    json_path = os.path.join(JSON_DIR, json_filename)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    return {
        "message": "Documents processed successfully",
        "json_file": json_path,
        "data": output
    }
