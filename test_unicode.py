#!/usr/bin/env python3
"""
Test script to verify Unicode character support in PDF generation
"""

import json
from pdf_generator import ConferencePDFGenerator

# Create test data with Hebrew characters
test_data = {
    "conference_title": "April 2025 General Conference",
    "talks": [
        {
            "title": "Test Talk with Hebrew Characters",
            "speaker": "Test Speaker",
            "author_role": "Test Role",
            "url": "/study/general-conference/2025/04/11test",
            "content": "The Hebrew word for faith is אמונה (emunah).\n\nThis is a test to ensure that Hebrew characters display correctly in the PDF instead of appearing as black boxes.\n\nHere are some more examples:\n- Hebrew: שלום (shalom - peace)\n- Greek: Χριστός (Christos - Christ)\n- Arabic: سلام (salam - peace)",
            "structured_content": [
                {
                    "type": "text",
                    "content": "The Hebrew word for faith is אמונה (emunah).\n\nThis is a test to ensure that Hebrew characters display correctly in the PDF instead of appearing as black boxes.\n\nHere are some more examples:\n- Hebrew: שלום (shalom - peace)\n- Greek: Χριστός (Christos - Christ)\n- Arabic: سلام (salam - peace)"
                }
            ],
            "footnotes": []
        }
    ]
}

# Generate PDF
print("Generating test PDF with Unicode characters...")
generator = ConferencePDFGenerator(test_data)
generator.generate_pdf("test_unicode_output.pdf")
print("\nTest PDF generated: test_unicode_output.pdf")
print("Please open the PDF and verify that Hebrew characters (אמונה) display correctly.")

