def merge_documents(doc_results):
    """
    Merge multiple document extraction results into a single person profile.
    """

    profile = {
        "name": None,
        "dob": None,
        "sources": [],
        "conflicts": []
    }

    for doc in doc_results:
        fields = doc.get("fields", {})
        source = doc.get("source_image")

        # NAME
        if fields.get("name"):
            if profile["name"] is None:
                profile["name"] = fields["name"]
                profile["sources"].append(source)
            elif profile["name"] != fields["name"]:
                profile["conflicts"].append({
                    "field": "name",
                    "values": [profile["name"], fields["name"]],
                    "source": source
                })

        # DOB
        if fields.get("dob"):
            if profile["dob"] is None:
                profile["dob"] = fields["dob"]
                profile["sources"].append(source)
            elif profile["dob"] != fields["dob"]:
                profile["conflicts"].append({
                    "field": "dob",
                    "values": [profile["dob"], fields["dob"]],
                    "source": source
                })

    return profile
