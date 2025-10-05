#!/usr/bin/env python3
"""
Test script to verify PDF bookmarks/outline functionality
"""

import json
from pdf_generator import ConferencePDFGenerator

# Create minimal test data
test_data = {
    "conference_title": "April 2025 General Conference",
    "talks": [
        {
            "title": "Test Talk 1",
            "speaker": "Speaker One",
            "author_role": "Test Role 1",
            "url": "/study/general-conference/2025/04/11test1",
            "content": "This is the first test talk content. It should appear under Saturday Morning Session.\n\nThis is a second paragraph to test formatting.",
            "structured_content": [],
            "footnotes": []
        },
        {
            "title": "Test Talk 2",
            "speaker": "Speaker Two",
            "author_role": "Test Role 2",
            "url": "/study/general-conference/2025/04/12test2",
            "content": "This is the second test talk content. It should also appear under Saturday Morning Session.\n\nAnother paragraph here.",
            "structured_content": [],
            "footnotes": []
        },
        {
            "title": "Test Talk 3",
            "speaker": "Speaker Three",
            "author_role": "Test Role 3",
            "url": "/study/general-conference/2025/04/21test3",
            "content": "This is the third test talk content. It should appear under Saturday Afternoon Session.\n\nMore content here.",
            "structured_content": [],
            "footnotes": []
        },
        {
            "title": "Test Talk 4",
            "speaker": "Speaker Four",
            "author_role": "Test Role 4",
            "url": "/study/general-conference/2025/04/41test4",
            "content": "This is the fourth test talk content. It should appear under Sunday Morning Session.\n\nFinal paragraph.",
            "structured_content": [],
            "footnotes": []
        }
    ]
}

# Generate PDF
print("Generating test PDF with bookmarks...")
generator = ConferencePDFGenerator(test_data)
generator.generate_pdf("test_bookmarks.pdf")

print("\nTest PDF generated: test_bookmarks.pdf")
print("Open it in a PDF reader and check the bookmarks/outline panel to see:")
print("  - Saturday Morning Session")
print("    - Speaker One: Test Talk 1")
print("    - Speaker Two: Test Talk 2")
print("  - Saturday Afternoon Session")
print("    - Speaker Three: Test Talk 3")
print("  - Sunday Morning Session")
print("    - Speaker Four: Test Talk 4")

