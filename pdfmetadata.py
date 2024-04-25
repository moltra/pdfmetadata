import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog, ttk

# Define data_folder as a global variable
data_folder = ""

def run():
    global data_folder  # Declare data_folder as global inside the function
    # Get the selected directory using a file dialog
    data_folder = filedialog.askdirectory()
    if not data_folder:  # If the user cancels the selection, display a message and return
        status_var.set("No directory selected.")
        return
    
    # Clear the treeview
    for row in treeview.get_children():
        treeview.delete(row)
    
# Iterate over PDF files in the data folder
for filename in os.listdir(data_folder):
    if filename.endswith(".pdf"):  # Check if the file is a PDF
        filepath = os.path.join(data_folder, filename)  # Full path to the PDF file

        # Open the PDF file in read mode
        with open(filepath, "rb") as pdf_file:
            # Create a PdfFileReader object to read the PDF
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)

            # Get the initial document information
            initial_info = pdf_reader.getDocumentInfo()

            # Create a PdfFileWriter object to update metadata
            pdf_writer_with_metadata = PyPDF2.PdfFileWriter()

            # Update metadata: set title as filename without extension
            for i in range(pdf_reader.numPages):
                page = pdf_reader.getPage(i)
                page.setTitle(os.path.splitext(filename)[0])
                pdf_writer_with_metadata.addPage(page)

            # Write the modified PDF to a new file
            output_filepath = os.path.join(data_folder, f"modified_{filename}")
            with open(output_filepath, "wb") as output_pdf_file:
                pdf_writer_with_metadata.write(output_pdf_file)

            # Reopen the modified PDF file to get final document information
            with open(output_filepath, "rb") as modified_pdf_file:
                modified_pdf_reader = PyPDF2.PdfFileReader(modified_pdf_file)
                final_info = modified_pdf_reader.getDocumentInfo()

            # Insert the initial and final metadata into the treeview
            treeview.insert("", "end", values=[filename, initial_info.title, final_info.title])
    # Display status
    status_var.set("Metadata cleaning complete.")

# Create the Tkinter root window
root = tk.Tk()
root.title("Metadata Cleaner")  # Set window title
root.geometry("500x400")  # Set window size

# Create a 'Run' button
run_button = tk.Button(root, text="Run", command=run)
run_button.pack()

# Create a label for displaying status
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var)
status_label.pack()

# Create a treeview to display metadata
treeview = ttk.Treeview(root, columns=("Filename", "Initial Metadata", "Final Metadata"), show="headings")
treeview.heading("Filename", text="Filename")
treeview.heading("Initial Metadata", text="Initial Metadata")
treeview.heading("Final Metadata", text="Final Metadata")
treeview.pack()

# Start the Tkinter event loop
root.mainloop()
