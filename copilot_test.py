import os
import logging
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfFileWriter, PdfFileReader
import tempfile

def get_metadata(folder_path):
    """
    Function to get metadata from all PDF files in a given folder.

    Parameters:
    folder_path (str): Path to the folder containing the PDF files.

    Returns:
    list: A list of tuples, each containing the title, author, and subject of a PDF file.
    """
    metadata = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "rb") as file:
                pdf = PdfFileReader(file)
                info = pdf.getDocumentInfo()
                title = os.path.splitext(filename)[0]
                metadata.append((title, info.author, info.subject))
    return metadata

# Set up logging to a file named 'log.txt'
logging.basicConfig(filename='log.txt', level=logging.INFO)


def display_metadata():
    """
    Function to display metadata from all PDF files in a selected folder in a tkinter GUI.
    The metadata before and after changes are displayed in a table format.
    The metadata are also written to a log file.
    """
    # Close any existing Tkinter windows
    for window in tk._default_root.winfo_children():
        window.destroy()

    # Create a new Tkinter window with a size of 350x350 pixels
    root = tk.Tk()
    root.geometry("350x350")

    # Open a folder selection dialog
    folder_path = filedialog.askdirectory()
    if folder_path:
        # Get the metadata before and after changes
        metadata_before = get_metadata(folder_path)
        change_metadata(folder_path)
        metadata_after = get_metadata(folder_path)
        
        # Create a Treeview widget to display the metadata in a table format
        tree = tk.Treeview(root)
        tree["columns"]=("before", "after")
        tree.column("#0", width=270, minwidth=270, stretch=False)
        tree.column("before", width=150, minwidth=150, stretch=True)
        tree.column("after", width=400, minwidth=200)
        
        tree.heading("#0",text="Name",anchor='w')
        tree.heading("before", text="Before Changes",anchor='w')
        tree.heading("after", text="After Changes",anchor='w')

        for data_before, data_after in zip(metadata_before, metadata_after):
            # Convert the metadata to a string and display it in the Treeview widget
            data_before_str = str(data_before)
            data_after_str = str(data_after)
            tree.insert("", 0, text="Metadata", values=(data_before_str, data_after_str))
            
            # Also write the metadata to the log file
            logging.info(f'Before: {data_before_str}, After: {data_after_str}')

        tree.pack()

    # Start the Tkinter event loop
    root.mainloop()

def change_metadata(folder_path):
    """
    Function to change the metadata of all PDF files in a given folder.
    The title of the metadata is changed to the filename without the extension.
    The rest of the metadata is cleared.

    Parameters:
    folder_path (str): Path to the folder containing the PDF files.
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "rb") as file:
                pdf = PdfFileReader(file)
                if pdf.getNumPages() > 0:  # Check if the PDF has at least one page
                    writer = PdfFileWriter()
                    writer.add_page(pdf.getPage(0))

                    # Change the title to the filename without the extension
                    title = os.path.splitext(filename)[0]
                    # Clear the rest of the metadata
                    metadata = {"Title": title, "Author": "", "Subject": "", "Producer": ""}

                    writer.add_metadata(metadata)

                    # Write the changes to a temporary file
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        writer.write(temp_file)

                    # Replace the original file with the temporary file
                    os.remove(file_path)
                    os.rename(temp_file.name, file_path)

# Create a tkinter root window
root = tk.Tk()
# Create a button that calls the display_metadata function when clicked
button = tk.Button(root, text="Select Folder", command=display_metadata)
button.pack()
# Start the tkinter main loop
root.mainloop()