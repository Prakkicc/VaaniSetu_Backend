def detect_document_type(text_lines):
    text = " ".join(text_lines).lower()

    birth_signals = [
        "date of birth",
        "date ofbirth",
        "dob",
        "d0b",
        "birth",
        "male",
        "female",
        "government of india"
    ]

    score = 0
    for signal in birth_signals:
        if signal in text:
            score += 1

    # Debug (optional, helps tuning)
    # print("Birth score:", score)

    if score >= 2:
        return "Birth Certificate"

    return "Unknown Document"
