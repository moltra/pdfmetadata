import os
import tkinter as tk
from tkinter import filedialog

import PyPDF2

import PyPDF2


def clear_metadata(document_info):
    """Clears all metadata except the title."""
    title = document_info.get('/Title', '')
    document_info.clear()
    document_info['/Title'] = title

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

                # Get the document information
                document_info = pdf_reader.getDocumentInfo()

                # Clear metadata except the title and replace the title with the filename without extension
                clear_metadata(document_info)
                document_info['/Title'] = os.path.splitext(filename)[0]

                # Display current metadata
                status_var.set(f"Metadata for {filename}: {document_info}")
                root.update()  # Update the GUI
                root.after(1000)  # Delay for 1 second (1000 milliseconds) before processing the next file

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
