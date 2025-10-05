#!/usr/bin/env python3
"""
Verify that the PDF doesn't have duplicate "Notes" text
"""

from PyPDF2 import PdfReader

pdf_path = "Output/test_notes_fix.pdf"

print(f"Checking PDF: {pdf_path}\n")

try:
    reader = PdfReader(pdf_path)
    
    # Check a few pages that should have footnotes
    pages_to_check = [3, 4, 5, 6, 7]  # First few talk pages
    
    for page_num in pages_to_check:
        if page_num < len(reader.pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            
            # Count occurrences of "Notes"
            notes_count = text.count("Notes")
            
            if notes_count > 1:
                print(f"Page {page_num + 1}: ⚠ WARNING - Found {notes_count} occurrences of 'Notes'")
                # Show context
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if 'Notes' in line:
                        print(f"  Line {i}: {line}")
            elif notes_count == 1:
                print(f"Page {page_num + 1}: ✓ Found 1 'Notes' header (correct)")
            else:
                print(f"Page {page_num + 1}: No 'Notes' found (no footnotes on this page)")
    
    print("\n✓ Verification complete!")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nNote: PyPDF2 might not be installed. Install with: pip install PyPDF2")

