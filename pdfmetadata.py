import os

import PyPDF2

# Directory containing PDF files
data_folder = "data"

# Iterate over PDF files in the data folder
for filename in os.listdir(data_folder):
    if filename.endswith(".pdf"):  # Check if the file is a PDF
        filepath = os.path.join(data_folder, filename)  # Full path to the PDF file

        # Open the PDF file in read mode
        with open(filepath, "rb") as pdf_file:
            # Create a PdfFileReader object
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)

            # Get the document information
            document_info = pdf_reader.getDocumentInfo()

            # Display current metadata
            print(f"Metadata for {filename}:")
            for key, value in document_info.items():
                print(f"{key}: {value}")
            print()  # Add a blank line for clarity between files
