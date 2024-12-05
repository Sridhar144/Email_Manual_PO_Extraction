from transformers import pipeline

def iterative_classification(subject, body, none_img_excel, classifier=None, max_length=512):
    subject_keywords = ["purchase order", "PO", "order"]
    body_keywords = ["Vendor", "Item", "Rate", "Quantity"]

    # Keyword-based classification for subject
    if any(keyword.lower() in subject.lower() for keyword in subject_keywords):
        return "PO", 0.9  # High confidence if keywords are present in subject

    # Function to truncate text at token level using the classifier's tokenizer
    def truncate_text(text, max_length, tokenizer):
        """
        Truncates the text to fit within the model's maximum sequence length using the tokenizer.
        """
        if tokenizer:  # Tokenize and truncate
            tokens = tokenizer(text, truncation=True, max_length=max_length, return_tensors="pt")
            return tokenizer.decode(tokens["input_ids"][0], skip_special_tokens=True)
        return text  # If no tokenizer, return the text as is (for testing)

    # Check if the classifier is provided
    if classifier:
        tokenizer = classifier.tokenizer  # Get the tokenizer from the classifier pipeline
    else:
        tokenizer = None  # For testing without a classifier

    # Truncate the body
    truncated_body = truncate_text(body, max_length, tokenizer)

    # Use body content for additional classification
    if classifier:
        body_result = classifier(truncated_body)[0]
        score = body_result.get("score", 0.5)
    else:
        body_result = {"label": "LABEL_0", "score": 0.5}
        score = 0.5

    if any(keyword.lower() in body.lower() for keyword in body_keywords):
        return "PO", max(score, 0.8)  # Increase confidence if keywords are present in body

    return "Not PO", score

from transformers import pipeline

def iterative_classification2(subject, body, classifier=None, max_length=512):
    subject_keywords = ["purchase order", "PO", "order"]
    body_keywords = ["Vendor", "Item", "Rate", "Quantity"]

    # Keyword-based classification for subject
    if any(keyword.lower() in subject.lower() for keyword in subject_keywords):
        return "PO", 0.9  # High confidence if keywords are present in subject

    # Function to truncate text at token level using the classifier's tokenizer
    def truncate_text(text, max_length, tokenizer):
        """
        Truncates the text to fit within the model's maximum sequence length using the tokenizer.
        """
        if tokenizer:  # Tokenize and truncate
            tokens = tokenizer(text, truncation=True, max_length=max_length, return_tensors="pt")
            return tokenizer.decode(tokens["input_ids"][0], skip_special_tokens=True)
        return text  # If no tokenizer, return the text as is (for testing)

    # Check if the classifier is provided
    if classifier:
        tokenizer = classifier.tokenizer  # Get the tokenizer from the classifier pipeline
    else:
        tokenizer = None  # For testing without a classifier

    # Truncate the body
    truncated_body = truncate_text(body, max_length, tokenizer)

    # Use body content for additional classification
    if classifier:
        body_result = classifier(truncated_body)[0]
        score = body_result.get("score", 0.5)
    else:
        body_result = {"label": "LABEL_0", "score": 0.5}
        score = 0.5

    if any(keyword.lower() in body.lower() for keyword in body_keywords):
        return "PO", max(score, 0.8)  # Increase confidence if keywords are present in body

    return "Not PO", score
