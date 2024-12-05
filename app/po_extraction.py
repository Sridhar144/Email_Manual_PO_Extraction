import re

def extract_po_details(text, text_gen_model):
    """
    Extracts Purchase Order details from email content using Llama 3.2B.
    :param text: The email body or parsed attachment text
    :param text_gen_model: Pretrained Llama 3.2B text-generation pipeline
    :return: Dictionary containing extracted PO details
    """
    extraction_prompt = (
        f"Extract structured purchase order details from the following text:\n\n{text}\n\n"
        "Provide the output in the following format:\n"
        "- Customer PO Number:\n"
        "- Item Names:\n"
        "- Quantities:\n"
        "- Rate per Unit:\n"
        "- Units of Measurement:\n"
        "- Delivery Dates:\n"
        "- Customer Name:\n"
    )

    result = text_gen_model(extraction_prompt, max_length=500, num_return_sequences=1)
    extracted_text = result[0]["generated_text"]

    po_details = {
        "Customer PO Number": re.search(r"Customer PO Number:\s*(.*)", extracted_text).group(1),
        "Item Names": re.findall(r"Item Names:\s*(.*)", extracted_text),
        "Quantities": re.findall(r"Quantities:\s*(.*)", extracted_text),
        "Rate per Unit": re.findall(r"Rate per Unit:\s*(.*)", extracted_text),
        "Units of Measurement": re.findall(r"Units of Measurement:\s*(.*)", extracted_text),
        "Delivery Dates": re.findall(r"Delivery Dates:\s*(.*)", extracted_text),
        "Customer Name": re.search(r"Customer Name:\s*(.*)", extracted_text).group(1),
    }

    return po_details
