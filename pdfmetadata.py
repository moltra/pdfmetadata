import os
import tkinter as tk
from tkinter import filedialog

import PyPDF2

import PyPDF2


def run():
    """Function to execute when the 'Run' button is clicked.

    This function prompts the user to select a directory containing PDF files
    using a file dialog. It then iterates over the PDF files in the selected
    directory, updates the metadata of each PDF file to set the title as the
    filename without extension, and saves the modified PDF files with a
    'modified_' prefix in the same directory.

    """
    # Get the selected directory using a file dialog
    data_folder = filedialog.askdirectory()
    if not data_folder:  # If the user cancels the selection, display a message and return
        status_var.set("No directory selected.")
        return
    
    # Iterate over PDF files in the data folder
    for filename in os.listdir(data_folder):
        if filename.endswith(".pdf"):  # Check if the file is a PDF
            filepath = os.path.join(data_folder, filename)  # Full path to the PDF file

            # Open the PDF file in read mode
            with open(filepath, "rb") as pdf_file:
                # Create a PdfFileReader object to read the PDF
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                pdf_writer = PyPDF2.PdfFileWriter()

                # Iterate over each page in the PDF
                for page_num in range(pdf_reader.numPages):
                    page = pdf_reader.getPage(page_num)
                    pdf_writer.add_page(page)
                
                # Get the document information
                document_info = pdf_reader.getDocumentInfo()

                # Create a PdfFileWriter object to update metadata
                pdf_writer_with_metadata = PyPDF2.PdfFileWriter()
                pdf_writer_with_metadata.addMetadata(document_info)

                # Update metadata: set title as filename without extension
                pdf_writer_with_metadata.set_information(pdf_writer_with_metadata.getNumPages() - 1, '/Title', os.path.splitext(filename)[0])

                # Write the modified PDF to a new file
                output_filepath = os.path.join(data_folder, f"modified_{filename}")
                with open(output_filepath, "wb") as output_pdf_file:
                    pdf_writer_with_metadata.write(output_pdf_file)

                # Display status
                status_var.set(f"Metadata updated for {filename}")
                root.update()  # Update the GUI

# Create the Tkinter root window
root = tk.Tk()
root.title("Metadata Cleaner")  # Set window title
root.geometry("200x200")  # Set window size

# Create a label for displaying status
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var)
status_label.pack()

# Create a 'Run' button
run_button = tk.Button(root, text="Run", command=run)
run_button.pack()

# Start the Tkinter event loop
root.mainloop()
