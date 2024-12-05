
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd1eacbf89c705ef49c1b4ff65d9e1c9a44097b861a589b2d720b13e0f6f89bcb'  # Replace with a strong secret key
app.config['UPLOAD_FOLDER'] = 'tests/sample files'      # Define a folder for handling uploaded files


from app.ui import ui_app


app.register_blueprint(ui_app)


__all__ = [
    "email_handler",
    "file_parser",
    "po_extraction",
    "iterative_classifier",
    "ui",
    "google_docs_parser"
]
