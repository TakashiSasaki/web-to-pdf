# Script Name: analyze_pdf_tags.py

import fitz  # PyMuPDF

def analyze_pdf_tags(pdf_path):
    doc = fitz.open(pdf_path)
    print(f"Analyzing PDF: {pdf_path}")
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        
        print(f"\nPage {page_num + 1} structure:")
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        font = span["font"]
                        print(f"Text: {text}, Font: {font}")

def main():
    pdf_files = ['sample.pdf', 'example.net.pdf']
    
    for pdf_file in pdf_files:
        analyze_pdf_tags(pdf_file)

if __name__ == "__main__":
    main()