#!/usr/bin/env python3
"""Extract text from PDFs and images, save as separate text files."""

import os
import sys
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("Installing PyPDF2...")
    os.system("pip install PyPDF2")
    import PyPDF2

try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("Installing Pillow and pytesseract...")
    os.system("pip install Pillow pytesseract")
    from PIL import Image
    import pytesseract

def extract_pdf_text(pdf_path):
    """Extract text from a PDF file."""
    text_content = []
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            print(f"  Processing {num_pages} pages...")
            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(f"\n--- Page {page_num} ---\n")
                        text_content.append(text)
                except Exception as e:
                    print(f"    Warning: Could not extract page {page_num}: {e}")
            
        return "\n".join(text_content)
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def extract_image_text(image_path):
    """Extract text from an image using OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text if text.strip() else "No text found in image"
    except Exception as e:
        return f"Error extracting image text: {str(e)}"

def process_files(source_dir, output_dir):
    """Process all PDFs and images in source directory."""
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all PDFs
    pdf_files = list(source_path.glob("*.pdf"))
    # Find all images
    image_files = list(source_path.glob("*.png")) + \
                  list(source_path.glob("*.jpg")) + \
                  list(source_path.glob("*.jpeg"))
    
    print(f"Found {len(pdf_files)} PDF(s) and {len(image_files)} image(s)")
    print()
    
    # Process PDFs
    for pdf_file in pdf_files:
        print(f"Processing PDF: {pdf_file.name}")
        text = extract_pdf_text(pdf_file)
        
        output_file = output_path / f"{pdf_file.stem}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Source: {pdf_file.name}\n")
            f.write("=" * 80 + "\n\n")
            f.write(text)
        
        print(f"  ✓ Saved to: {output_file}\n")
    
    # Process images
    for image_file in image_files:
        print(f"Processing image: {image_file.name}")
        text = extract_image_text(image_file)
        
        output_file = output_path / f"{image_file.stem}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Source: {image_file.name}\n")
            f.write("=" * 80 + "\n\n")
            f.write(text)
        
        print(f"  ✓ Saved to: {output_file}\n")
    
    print(f"✓ All files processed! Text files saved to: {output_path}")

if __name__ == "__main__":
    # Process files from current directory and ted-nelson-clone directory
    base_dir = Path(__file__).parent
    output_dir = base_dir / "ted-nelson-clone" / "extracted-text"
    
    print("Extracting text from PDFs and images...")
    print("=" * 80)
    print()
    
    # Process root directory files
    print("Processing files in root directory:")
    process_files(base_dir, output_dir)
    
    # Process ted-nelson-clone directory files
    clone_dir = base_dir / "ted-nelson-clone"
    if clone_dir.exists():
        print("\nProcessing files in ted-nelson-clone directory:")
        process_files(clone_dir, output_dir)

