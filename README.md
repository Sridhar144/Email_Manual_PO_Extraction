**Email, Manual Purchase Order Extraction**

This repository contains the solution for the AI Intern task, which focuses on email classification and extraction of Purchase Order (PO) details from emails. The system uses machine learning models and various Python libraries to classify emails and extract useful data.

**Setup Instructions**

**Clone the repository:**

1\. **Install Dependencies:** The following Python libraries are required to run the system:

- Flask
- transformers
- imaplib
- email
- pandas
- PyPDF2
- pytesseract
- Pillow
- docx
- openai (if using GPT model)

To install them, run: 

pip install -r requirements.txt

2\.

3\. **Setup Environment:**

- You need to have access to an email server that supports IMAP for fetching emails (e.g., Gmail, Outlook).
- Set up a .env file![](Aspose.Words.1a8e351d-6e1c-4a52-b439-5abf22b1bb2c.002.png)

**Approach**

1. **Email Fetching and Classification:**
- The system connects to an email server via IMAP, retrieves emails, and extracts their content (subject, body, and attachments).
- A classifier model is used to identify whether the email is a Purchase Order (PO) or not.
2. **PO Extraction:**
- If the email is classified as a PO, the system parses the body of the email for key information such as PO number, product details, quantities, and total order value.
3. **Attachments Handling:**
- Attachments such as PDFs, images, DOCX files, and Excel sheets are extracted and parsed as necessary.

**Key Challenges Faced**

- **Model Accuracy**: Ensuring the email classifier correctly identifies POs amidst other email types.
- **Data Extraction**: Extracting structured information (PO number, products, quantities) from unstructured email bodies.
- **Handling Attachments**: Parsing different attachment formats (PDF, image, Excel) with correct handling for each type.

**Test Cases and Coverage**

The system was tested with a variety of test cases to ensure robustness. Below are the key test cases:

- **Test Case 1**: Classifying emails with valid PO formats.
  **Expected Result**: The email is classified as "PO" and PO details are extracted.
  **Status**: Passed
- **Test Case 2**: Classifying non-PO emails (e.g., newsletters, personal emails).
  **Expected Result**: The email is classified as not a "PO".
  **Status**: Passed
- **Test Case 3**: Handling emails with attachments (PDF, images, Excel).
  **Expected Result**: Attachments are correctly extracted and parsed.
  **Status**: Passed
- **Test Case 4**: Invalid email formats or missing PO information.
  **Expected Result**: The system returns an appropriate error or fallback message.
  **Status**: Passed

**How to Use**

Start the Flask application: 

python app.py

1. Open the application in your browser (typically at http://127.0.0.1:5000).
1. Submit email details via the form, or allow the system to fetch and classify emails from the connected inbox.

