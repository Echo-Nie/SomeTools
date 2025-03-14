import os
import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF


def extract_images_from_pdf(pdf_path, output_folder):
    """
    Extract pictures from PDF files and save to xx folders
    """

    try:
        # open PDF
        pdf_document = fitz.open(pdf_path)
        image_count = 0

        # for each page of the PDF
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            image_list = page.get_images()

            # for each pictures
            for image_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # save pictures
                image_filename = f"image_page{page_number + 1}_index{image_index + 1}.{image_ext}"
                image_path = os.path.join(output_folder, image_filename)
                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)
                image_count += 1

        return image_count
    except Exception as e:
        raise e


def browse_files():
    """
    open GUI
    """
    file_paths = filedialog.askopenfilenames(
        title="select PDF", filetypes=[("PDF File", "*.pdf")]
    )
    file_paths = root.tk.splitlist(file_paths)
    file_listbox.delete(0, tk.END)
    for file_path in file_paths:
        file_listbox.insert(tk.END, file_path)

def browse_folder():
    """
    select output folder
    """
    folder_path = filedialog.askdirectory(title="select output folder")
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(tk.END, folder_path)

def extract_images():
    """
    the main function to extract
    """
    # get the pdf and folder selected
    pdf_files = file_listbox.get(0, tk.END)
    output_folder = output_folder_entry.get()

    if not pdf_files:
        messagebox.showwarning("warning", "please select PDF file!")
        return

    if not output_folder:
        messagebox.showwarning("warning", "the output folder is null!")
        return

    # for each pdf to get the pictures
    total_images = 0
    for pdf_file in pdf_files:
        try:
            image_count = extract_images_from_pdf(pdf_file, output_folder)
            total_images += image_count
            messagebox.showinfo(
                "Success", f"{image_count} images extracted from file {pdf_file}!"
            )
        except Exception as e:
            messagebox.showerror("Fail", f"Error processing file {pdf_file}: {str(e)}")
            return

    messagebox.showinfo("Finish", f"A total of {total_images} images were extracted!")


# create main window
root = tk.Tk()
root.title("Image extraction tool")

# select files
file_frame = tk.Frame(root)
file_frame.pack(pady=10)

file_label = tk.Label(file_frame, text="select PDF file：")
file_label.pack(side=tk.LEFT)

browse_button = tk.Button(file_frame, text="Select", command=browse_files)
browse_button.pack(side=tk.LEFT, padx=10)

file_listbox = tk.Listbox(root, width=50, height=10)
file_listbox.pack(pady=10)

# Output folder selection
output_frame = tk.Frame(root)
output_frame.pack(pady=10)

output_label = tk.Label(output_frame, text="select output folder：")
output_label.pack(side=tk.LEFT)

output_folder_entry = tk.Entry(output_frame, width=30)
output_folder_entry.pack(side=tk.LEFT, padx=10)

folder_browse_button = tk.Button(output_frame, text="Select", command=browse_folder)
folder_browse_button.pack(side=tk.LEFT)

# Extract the picture
extract_button = tk.Button(root, text="Extract the picture", command=extract_images)
extract_button.pack(pady=10)

# run the main
root.mainloop()