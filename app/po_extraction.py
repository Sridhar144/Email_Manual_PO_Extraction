import re
from collections import defaultdict

def extract_po_details(text, none_img_excel, text_gen_model=None):
    if none_img_excel==0:
        print(f'hello {text}, {text_gen_model}')
        """
        Extract Purchase Order details from email content using regex and structured parsing.
        :param text: The email body or parsed attachment text
        :param text_gen_model: Optional, pretrained text-generation model for fallback
        :return: Dictionary containing extracted PO details
        """
        po_details = defaultdict(list)

        # Regex patterns for key fields
        patterns = {
            "Customer PO Number": r"(?:Purchase Order No:|PO Number)[:\s]*(\w+)",
            "Vendor Name": r"Vendor Name:([\w\s,.-]+)",
            "Items": r"(\d+\s+[\w\s\-()]+[\d.,]+[\d.,]+)",
            "Taxable Amount": r"Taxable Amount[:\s]*(\d+,\d+\.\d+|\d+\.\d+)",
            "Total Amount": r"GRAND TOTAL[:\s]*(\d+,\d+\.\d+|\d+\.\d+)",
        }
        print("1")
        # Extract fields using regex
        for field, pattern in patterns.items():
            match = re.findall(pattern, text)
            print("2 ", match, pattern)
            if match:
                po_details[field] = match if len(match) > 1 else match[0]
        print("3")

        # Extract items and format as structured data
        item_pattern = r"(\d+)\s([\w\s\-()]+)\s([\d,.]+)\s([\w]+)\s([\d,.]+)\s([\d,.]+)"
        items = re.findall(item_pattern, text)
        print(items)
        for item in items:
            print ("5", items)
            po_details["Items"].append({
                "Sr No": item[0],
                "Description": item[1],
                "Quantity": item[2],
                "Unit": item[3],
                "Rate": item[4],
                "Amount": item[5],
            })
        print("6")
        if items==[] or items.count==0:
            return None
        # Optional: Use text generation model for fallback
        if text_gen_model and not po_details:
            extraction_prompt = (
                f"Extract structured purchase order details from the following text:\n\n{text}\n\n"
                "Provide the output in a JSON format with keys like 'PO Number', 'Vendor Name', 'Items', etc."
            )
            result = text_gen_model(extraction_prompt, max_length=500, num_return_sequences=1)
            po_details = result[0]["generated_text"]

        return dict(po_details)
    elif none_img_excel==1:
        """
        Extract Purchase Order details from email content using regex and structured parsing.
        :param text: The email body or parsed attachment text
        :param text_gen_model: Optional, pretrained text-generation model for fallback
        :return: Dictionary containing extracted PO details
        """
        po_details = defaultdict(list)

        # Updated regex patterns
        patterns = {
            "Customer PO Number": r"(?:PO|Purchase Order|PO No\.?)\s*(\w+\d+)",
            "Vendor Name": r"From:\s*([\w\s]+)<",
        }

        # Extract fields using regex
        for field, pattern in patterns.items():
            match = re.findall(pattern, text)
            if match:
                po_details[field] = match if len(match) > 1 else match[0]

        # Debug extracted fields
        print("Extracted Fields:", po_details)

        # If items or attachments are not well-structured, you might need fallback logic
        item_pattern = r"(\d+)\)\s([\w\s]+)\s([\d,.]+)\s([\d,.]+)"
        items = re.findall(item_pattern, text)
        for item in items:
            po_details["Items"].append({
                "Sr No": item[0],
                "Description": item[1],
                "Quantity": item[2],
                "Amount": item[3],
            })

        # Fallback to text generation model if no details found
        if text_gen_model and not po_details:
            extraction_prompt = (
                f"Extract structured purchase order details from the following text:\n\n{text}\n\n"
                "Provide the output in a JSON format with keys like 'PO Number', 'Vendor Name', 'Items', etc."
            )
            result = text_gen_model(extraction_prompt, max_length=500, num_return_sequences=1)
            po_details = result[0]["generated_text"]

        return dict(po_details)
