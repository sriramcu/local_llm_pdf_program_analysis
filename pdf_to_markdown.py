import os
import argparse
from PyPDF2 import PdfWriter, PdfReader
from utils import convert_pdf_to_markdown  # Importing the method from utils

def extract_single_page_to_temp_pdf(pdf_file, page_number):
    """
    Extracts a specific page from the PDF and saves it as a temporary PDF file.
    """
    try:
        temp_pdf_path = "temp_page.pdf"
        reader = PdfReader(pdf_file)
        writer = PdfWriter()

        if page_number < 1 or page_number > len(reader.pages):
            raise ValueError(f"Page number {page_number} is out of range for the given PDF.")

        # Add the specified page to a new PDF
        writer.add_page(reader.pages[page_number - 1])

        # Write the temporary PDF
        with open(temp_pdf_path, "wb") as temp_pdf:
            writer.write(temp_pdf)

        return temp_pdf_path
    except Exception as e:
        raise e

def main():
    parser = argparse.ArgumentParser(description="Convert a PDF or a specific page to Markdown.")
    parser.add_argument(
        'pdf_file', type=str, help="Path to the PDF file to be converted."
    )
    parser.add_argument(
        '--page', type=int, default=None, help="Page number to convert (optional). Default is entire PDF."
    )
    args = parser.parse_args()

    pdf_file = args.pdf_file
    page_number = args.page

    if not os.path.isfile(pdf_file):
        print(f"Error: The file '{pdf_file}' does not exist.")
        return

    try:
        if page_number:
            # Extract single page to temp PDF
            temp_pdf_path = extract_single_page_to_temp_pdf(pdf_file, page_number)
            try:
                markdown = convert_pdf_to_markdown(temp_pdf_path)
            finally:
                os.remove(temp_pdf_path)  # Ensure temp file is deleted
        else:
            # Convert entire PDF
            markdown = convert_pdf_to_markdown(pdf_file)
        
        print("Converted Markdown Content:")
        print(markdown)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
