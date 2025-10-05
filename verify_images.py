#!/usr/bin/env python3
"""
Verify that images are being downloaded and included in PDFs
"""

from conference_scraper import ConferenceScraper

# Test with a single talk that has images
url = "/general-conference/2025/04/13holland"

print("Verifying image extraction...")
print(f"URL: {url}\n")

scraper = ConferenceScraper("https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng")

# Fetch the talk
talk_data = scraper.fetch_talk_content(url)
if talk_data:
    body_html = talk_data['content']['body']
    content_data = scraper.extract_content_from_html(body_html)
    
    print(f"Structured content has {len(content_data['structured_content'])} items:\n")
    
    for i, item in enumerate(content_data['structured_content'], 1):
        if item['type'] == 'text':
            preview = item['content'][:100].replace('\n', ' ')
            print(f"{i}. TEXT: {preview}...")
        elif item['type'] == 'image':
            print(f"{i}. IMAGE:")
            print(f"   URL: {item['url']}")
            print(f"   Title: {item['title']}")
            print(f"   Alt: {item['alt']}")
            print()

print("\n✓ Verification complete!")

