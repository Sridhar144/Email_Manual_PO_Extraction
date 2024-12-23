import imaplib
import email
from email.header import decode_header
from .file_parser import save_attachment

def connect_to_email(username, password, imap_server):
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    return mail

def fetch_emails(mail, subject_line=None):
    mail.select("inbox")
    
    # If subject_line is provided, search for emails with that subject
    if subject_line:
        status, messages = mail.search(None, f'(SUBJECT "{subject_line}")')
    else:
        status, messages = mail.search(None, "ALL")
    
    email_ids = messages[0].split()
    emails = []
    for e_id in email_ids:
        _, msg = mail.fetch(e_id, "(RFC822)")
        emails.append(email.message_from_bytes(msg[0][1]))
    return emails

def extract_email_content(email_msg):
    subject = decode_header(email_msg["Subject"])[0][0]
    sender = email_msg["From"]
    body = ""
    attachments = []

    if email_msg.is_multipart():
        for part in email_msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body += part.get_payload(decode=True).decode()
            elif part.get("Content-Disposition"):
                filepath = save_attachment(part, "downloads/")
                attachments.append(filepath)
    else:
        body = email_msg.get_payload(decode=True).decode()
    return subject, sender, body, attachments
