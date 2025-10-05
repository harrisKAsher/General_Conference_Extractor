#!/usr/bin/env python3
"""
Debug script to see the actual HTML structure around footnotes
"""

from conference_scraper import ConferenceScraper

url = "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"

scraper = ConferenceScraper(url)
conference_data = scraper.fetch_conference_data()
html_body = conference_data['content']['body']
talks = scraper.parse_talk_links(html_body)

# Get first talk
talk = talks[0]
print(f"Fetching: {talk['speaker']}: {talk['title']}\n")
talk_data = scraper.fetch_talk_content(talk['url'])

if talk_data:
    body_html = talk_data['content']['body']
    
    # Find the "Notes" section in the HTML
    import re
    
    # Look for "Notes" near the footer
    notes_pattern = r'.{200}Notes.{200}'
    matches = re.findall(notes_pattern, body_html, re.DOTALL)
    
    if matches:
        print("Found 'Notes' in HTML:")
        for i, match in enumerate(matches, 1):
            print(f"\n--- Match {i} ---")
            print(match)
            print("--- End Match ---")
    
    # Also look for the footer tag
    footer_pattern = r'.{200}<footer.{200}'
    matches = re.findall(footer_pattern, body_html, re.DOTALL)
    
    if matches:
        print("\n\nFound '<footer' in HTML:")
        for i, match in enumerate(matches, 1):
            print(f"\n--- Match {i} ---")
            print(match)
            print("--- End Match ---")

