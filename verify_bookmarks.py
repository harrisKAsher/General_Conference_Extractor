#!/usr/bin/env python3
"""
Verify that PDF bookmarks/outlines are present in a PDF file
"""

import sys
try:
    from PyPDF2 import PdfReader
except ImportError:
    print("PyPDF2 not installed. Install with: pip install PyPDF2")
    sys.exit(1)

def print_bookmarks(bookmarks, indent=0):
    """Recursively print bookmarks"""
    if not bookmarks:
        return

    for item in bookmarks:
        if isinstance(item, list):
            # Nested list of bookmarks
            print_bookmarks(item, indent + 2)
        elif isinstance(item, dict):
            # Dictionary-style bookmark
            title = item.get('/Title', 'Untitled')
            print(" " * indent + f"- {title}")
        else:
            # PyPDF2 Destination object
            try:
                title = item.title if hasattr(item, 'title') else str(item)
                print(" " * indent + f"- {title}")
            except:
                print(" " * indent + f"- {item}")

def verify_pdf_bookmarks(pdf_path):
    """Verify bookmarks in a PDF file"""
    print(f"Checking bookmarks in: {pdf_path}\n")
    
    try:
        reader = PdfReader(pdf_path)
        
        # Get the outline (bookmarks)
        outlines = reader.outline
        
        if not outlines:
            print("❌ No bookmarks found in PDF")
            return False
        
        print("✅ Bookmarks found!\n")
        print("PDF Outline Structure:")
        print("=" * 50)
        print_bookmarks(outlines)
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python verify_bookmarks.py <pdf_file>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    verify_pdf_bookmarks(pdf_file)

