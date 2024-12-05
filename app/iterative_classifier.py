def iterative_classification(subject, body, classifier):
    subject_result = classifier(subject)[0]
    if subject_result["label"] == "LABEL_1" and subject_result["score"] > 0.8:
        return "PO", subject_result["score"]
    elif subject_result["score"] > 0.4:

        body_result = classifier(body)[0]
        return ("PO", body_result["score"]) if body_result["label"] == "LABEL_1" else ("Not PO", body_result["score"])
    return "Not PO", subject_result["score"]
