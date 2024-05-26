from PyPDF2 import PdfReader, PdfWriter
import os
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, messagebox, Frame, font
from tqdm import tqdm

def split_pages(input_file, output_dir, pages):
    with open(input_file, 'rb') as f:
        reader = PdfReader(f)
        writer = PdfWriter()
        page_indices = []

        if pages:
            for part in pages.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    page_indices.extend(range(start - 1, end))  # Convert to zero-based index
                else:
                    page_indices.append(int(part) - 1)  # Convert to zero-based index
        else:
            page_indices = range(len(reader.pages))  # Select all pages if no specific pages provided

        for page_num in page_indices:
            writer.add_page(reader.pages[page_num])

        pages_str = pages.replace(',', '_').replace('-', 'to') if pages else "all"
        output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_pages_{pages_str}.pdf")
        with open(output_file, 'wb') as output:
            writer.write(output)

def process_directory(input_dir, output_dir, pages):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
    for filename in tqdm(pdf_files, desc="Processing PDFs"):
        input_path = os.path.join(input_dir, filename)
        split_pages(input_path, output_dir, pages)

class PDFSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Splitter")
        
        self.input_dir = ""
        self.output_dir = ""
        self.pages = StringVar()

        self.label = Label(root, text="Select input and output directories, and specify pages to split")
        self.label.pack(pady=10)

        # Frame for input directory selection
        self.input_frame = Frame(root)
        self.input_frame.pack(pady=5)

        self.input_button = Button(self.input_frame, text="Select Input Folder", command=self.select_input_directory)
        self.input_button.pack(side='left')

        self.input_label = Label(self.input_frame, text="No input folder selected")
        self.input_label.pack(side='left', padx=10)

        # Frame for output directory selection
        self.output_frame = Frame(root)
        self.output_frame.pack(pady=5)

        self.output_button = Button(self.output_frame, text="Select Output Folder", command=self.select_output_directory)
        self.output_button.pack(side='left')

        self.output_label = Label(self.output_frame, text="No output folder selected")
        self.output_label.pack(side='left', padx=10)

        self.pages_label = Label(root, text="Pages to split (e.g., 1,3-5):")
        self.pages_label.pack(pady=5)

        self.pages_entry = Entry(root, textvariable=self.pages)
        self.pages_entry.pack(pady=5)

        self.process_button = Button(root, text="Start Processing", command=self.start_processing)
        self.process_button.pack(pady=20)

        self.clear_button = Button(root, text="Clear All", command=self.clear_all)
        self.clear_button.pack(pady=5)

    def select_input_directory(self):
        self.input_dir = filedialog.askdirectory(title='Select Input Directory')
        if self.input_dir:
            self.input_label.config(text=f"Selected input: {self.input_dir}")

    def select_output_directory(self):
        self.output_dir = filedialog.askdirectory(title='Select Output Directory')
        if self.output_dir:
            self.output_label.config(text=f"Selected output: {self.output_dir}")

    def start_processing(self):
        if self.input_dir and self.output_dir:
            self.label.config(text="Processing, please wait...")
            try:
                process_directory(self.input_dir, self.output_dir, self.pages.get())
                self.label.config(text="Processing complete!", fg="green", font=font.Font(size=20, weight='bold'))
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.label.config(text="Processing failed!")
        else:
            self.label.config(text="Please select both input and output directories")

    def clear_all(self):
        self.input_dir = ""
        self.output_dir = ""
        self.pages.set("")
        self.input_label.config(text="No input folder selected")
        self.output_label.config(text="No output folder selected")
        self.label.config(text="Select input and output directories, and specify pages to split", fg="black", font=font.Font(size=10, weight='normal'))

if __name__ == "__main__":
    root = Tk()
    app = PDFSplitterApp(root)
    root.mainloop()