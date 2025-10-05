#!/usr/bin/env python3
"""
Test script to verify image extraction and PDF generation with images
"""

from conference_scraper import ConferenceScraper
from pdf_generator import ConferencePDFGenerator
import os

# Test with a single talk that has images
url = "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"

print("Testing image extraction and PDF generation...")
print(f"URL: {url}\n")

scraper = ConferenceScraper(url)

# Get conference data
conference_data = scraper.fetch_conference_data()
html_body = conference_data['content']['body']
talk_links = scraper.parse_talk_links(html_body)

print(f"Found {len(talk_links)} talks total")
print("Testing with first talk that has images...\n")

# Find a talk with images
talks = []
for i, talk_info in enumerate(talk_links, 1):
    print(f"[{i}/{len(talk_links)}] {talk_info['speaker']}: {talk_info['title']}")
    
    talk_data = scraper.fetch_talk_content(talk_info['url'])
    if talk_data:
        body_html = talk_data['content']['body']
        content_data = scraper.extract_content_from_html(body_html)

        talk_info['content'] = content_data['text']
        talk_info['structured_content'] = content_data['structured_content']
        talk_info['full_data'] = talk_data

        # Count and display images
        images = [item for item in content_data['structured_content'] if item['type'] == 'image']
        if images:
            print(f"  ✓ Found {len(images)} image(s)")
            for img in images:
                print(f"    - {img['title'] or img['alt']}")
        
        talks.append(talk_info)

        # Stop after finding 2 talks with images
        talks_with_images = [t for t in talks if any(item['type'] == 'image' for item in t.get('structured_content', []))]
        if len(talks_with_images) >= 2:
            break

# Create test conference data
test_data = {
    'conference_title': conference_data['meta']['title'] + ' (Image Test)',
    'talks': talks
}

# Generate PDF
output_dir = "Output"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'test_images.pdf')

print("\nGenerating test PDF with images...")
generator = ConferencePDFGenerator(test_data)
generator.generate_pdf(output_file)

print(f"\n✓ Test complete! Check {output_file}")

