from src.multi_document_pipeline import process_multiple_documents

IMAGE_PATHS = [
    "data/raw/test.jpg",
    "data/raw/test2.jpg"  # add another doc
]

def main():
    results = process_multiple_documents(IMAGE_PATHS)

    print("\nMULTI-DOCUMENT RESULTS:\n")
    for res in results:
        print("-" * 40)
        for k, v in res.items():
            print(f"{k}: {v}")

if __name__ == "__main__":
    main()


