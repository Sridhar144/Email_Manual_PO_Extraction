from pathlib import Path
from flask import Flask, request, render_template
from .email_handler import extract_email_content, connect_to_email, fetch_emails
from .file_parser import save_attachment
from .iterative_classifier import iterative_classification, iterative_classification2
from .po_extraction import extract_po_details
from .setup_model import setup_llama
from flask import Blueprint
from dotenv import load_dotenv
import os
import pandas as pd

ui_app = Blueprint('ui', __name__)
app = Flask(__name__)
import os
text_gen_model, classifier = setup_llama()
downloads_folder = "downloads"
if not os.path.exists(downloads_folder):
    os.makedirs(downloads_folder)


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
IMAP_SERVER = os.getenv('SERVER')
USERNAME = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
print(USERNAME)
@ui_app.route("/", methods=["GET", "POST"])




def home():
    po_details = None
    classification = None
    score = None
    attachments = []
    none_img_excel=0
    if request.method == "POST":
        subject = request.form.get("subject")
        body = request.form.get("body")

        # Check if files are uploaded
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file:
                # Save and parse the uploaded file
                file_path = f"downloads/{file.filename}"
                file.save(file_path)
                ext = file_path.split('.')[-1]
                
                if ext in ["jpg", "jpeg", "png"]:
                    none_img_excel=1
                
                elif ext in ["xlsx", "xls"]:
                    none_img_excel=2
                attachments.append(save_attachment(file_path))  # Parse and store the content from attachment
        # Perform classification on the email content
        print(attachments)
        subject=body
        body=str()
        # if none_img_excel!=2:
        for attachment in attachments:
            if none_img_excel==2:
                flattened_data = []
                for row in attachment:
                    print("Row",  row)
                    for key, value in row.items():
                        print(f"{key}: {value}")
                        if pd.notna(value) and pd.notnull(value):  # Check if the value is not NaN
                            flattened_data.append(value)

                # Convert the list into a list of strings or a single string
                list_of_strings = [str(item) for item in flattened_data]  # List of strings
                single_string = " ".join(list_of_strings)  # Single string
                body+=single_string
            else:
                attachment=str(attachment)
                body+=attachment
        print("test", body)
        classification, score = iterative_classification(subject, body, none_img_excel, classifier)
        # if none_img_excel==2:
            
        print(classification, score)
        # If it's a Purchase Order (PO), extract PO details
        if classification == "PO":
            po_details = extract_po_details(body, none_img_excel, text_gen_model)
        
        return render_template("results.html", po_details=po_details, classification=classification, score=score, attachments=attachment)
    
    return render_template("index.html")


# New route for fetching and processing emails with a specific subject
@ui_app.route("/fetch-emails", methods=["GET", "POST"])
def fetch_emails_page():
    if request.method == "POST":
        # Get the subject line entered by the user
        subject_line = request.form.get("subject_line")
        print(subject_line)
        # Connect to the email server and fetch emails with the provided subject
        mail = connect_to_email(USERNAME, PASSWORD, IMAP_SERVER)
        emails = fetch_emails(mail, subject_line)
        print(mail, emails)
        # Process the first email (or all emails if needed)
        if emails:
            email_msg = emails[0]  # You can iterate over all emails if you need
            subject, sender, body, attachments = extract_email_content(email_msg)
            
            # Now classify the email content
            classification, score = iterative_classification(subject, body, classifier)
            
            # If it's a PO, extract the PO details
            if classification == "PO":
                po_details = extract_po_details(body, text_gen_model)
                return render_template("email_results.html", po_details=po_details, score=score, subject=subject, sender=sender, attachments=attachments)
            
            # Otherwise just show classification results
            return render_template("email_results.html", classification=classification, score=score, subject=subject, sender=sender, attachments=attachments)
        else:
            # If no emails match the subject
            return render_template("fetch_emails.html", error="No emails found with that subject.")
    
    return render_template("fetch_emails.html")
