import os
import tkinter as tk
from tkinter import filedialog

import PyPDF2

import PyPDF2


def clear_metadata(document_info):
    """Clears all metadata except the title."""
    title = document_info.title if '/Title' in document_info else ''
    document_info.clear()
    document_info.title = title

def run():
    """Function to execute when the 'Run' button is clicked."""
    # Get the selected directory
    data_folder = filedialog.askdirectory()
    if not data_folder:  # User canceled selection
        status_var.set("No directory selected.")
        return
    
    # Iterate over PDF files in the data folder
    for filename in os.listdir(data_folder):
        if filename.endswith(".pdf"):  # Check if the file is a PDF
            filepath = os.path.join(data_folder, filename)  # Full path to the PDF file

            # Open the PDF file in read mode
            with open(filepath, "rb") as pdf_file:
                # Create a PdfFileReader object
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                pdf_writer = PyPDF2.PdfFileWriter()

                # Iterate over each page in the PDF
                for page_num in range(pdf_reader.numPages):
                    page = pdf_reader.getPage(page_num)
                    pdf_writer.add_page(page)
                
                # Get the document information
                document_info = pdf_reader.getDocumentInfo()

                # Clear metadata except the title and replace the title with the filename without extension
                clear_metadata(document_info)
                document_info.title = os.path.splitext(filename)[0]

                # Add modified metadata
                pdf_writer.addMetadata(document_info)

                # Write the modified PDF to a new file
                output_filepath = os.path.join(data_folder, f"modified_{filename}")
                with open(output_filepath, "wb") as output_pdf_file:
                    pdf_writer.write(output_pdf_file)

                # Display status
                status_var.set(f"Metadata updated for {filename}")
                root.update()  # Update the GUI

# Create the Tkinter root window
root = tk.Tk()
root.title("PDF Metadata Editor")

# Create a label for displaying status
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var)
status_label.pack()

# Create a 'Run' button
run_button = tk.Button(root, text="Run", command=run)
run_button.pack()

# Start the Tkinter event loop
root.mainloop()
