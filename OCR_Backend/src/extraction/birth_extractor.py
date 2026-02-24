import re

def extract_birth_fields(lines):
    """
    Extract key fields from Birth Certificate OCR text lines.
    Handles both labeled and unlabeled Indian certificates.
    """

    data = {
        "name": None,
        "dob": None,
        "place_of_birth": None,
        "registration_no": None
    }

    # -------------------------
    # 1. NAME (STRICT: labeled)
    # -------------------------
    for line in lines:
        line_upper = line.upper()
        if line_upper.startswith("NAME"):
            val = line.split(":", 1)[-1].strip()
            val = re.sub(r"[^A-Z.\s]", "", val, flags=re.I)
            if val:
                data["name"] = val.strip()
                break

    # ---------------------------------------
    # 2. NAME (FALLBACK: unlabeled name line)
    # ---------------------------------------
    if data["name"] is None:
        for line in lines:
            line_clean = line.strip()

            if (
                line_clean.replace(" ", "").isalpha()
                and len(line_clean.split()) >= 2
                and not any(
                    keyword in line_clean.lower()
                    for keyword in [
                        "government",
                        "india",
                        "date",
                        "birth",
                        "dob",
                        "male",
                        "female",
                        "registration"
                    ]
                )
            ):
                data["name"] = line_clean
                break

    # -------------------------
    # 3. DATE OF BIRTH
    # -------------------------
    for line in lines:
        match = re.search(r"\b\d{2}/\d{2}/\d{4}\b", line)
        if match:
            data["dob"] = match.group(0)
            break

    # -------------------------
    # 4. PLACE OF BIRTH
    # -------------------------
    for i, line in enumerate(lines):
        if "PLACE OF BIRTH" in line.upper():
            for j in range(i + 1, min(i + 5, len(lines))):
                candidate = lines[j].strip()
                if (
                    any(c.isalpha() for c in candidate)
                    and not re.search(r"\d{2}/\d{2}/\d{4}", candidate)
                ):
                    data["place_of_birth"] = candidate
                    break
            break

    # -------------------------
    # 5. REGISTRATION NUMBER
    # -------------------------
    for i, line in enumerate(lines):
        if "REGISTRATION" in line.upper():
            for j in range(i + 1, min(i + 4, len(lines))):
                match = re.search(r"\d+[/\-]\d+", lines[j])
                if match:
                    data["registration_no"] = match.group(0)
                    break
            break

    return data
