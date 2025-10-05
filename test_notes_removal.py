#!/usr/bin/env python3
"""
Test to verify that "Notes" header is removed from body text
"""

from conference_scraper import ConferenceScraper

# Test with April 2025 conference
url = "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"

print("Testing Notes header removal...")
print(f"URL: {url}\n")

scraper = ConferenceScraper(url)

# Fetch conference data
conference_data = scraper.fetch_conference_data()
html_body = conference_data['content']['body']
talks = scraper.parse_talk_links(html_body)

# Test with first few talks that have footnotes
print("Looking for talks with footnotes...\n")
talks_tested = 0
for talk in talks[:10]:
    print(f"Testing: {talk['speaker']}: {talk['title']}")
    talk_data = scraper.fetch_talk_content(talk['url'])
    if talk_data:
        body_html = talk_data['content']['body']
        content_data = scraper.extract_content_from_html(body_html)

        if content_data.get('footnotes'):
            print(f"  ✓ Found {len(content_data['footnotes'])} footnote(s)")

            # Check if "Notes" appears in the text
            full_text = content_data['text']

            # Check for "Notes" as a standalone word (case-insensitive)
            import re
            notes_pattern = r'\bNotes\b'
            matches = re.findall(notes_pattern, full_text, re.IGNORECASE)

            if matches:
                print(f"  ⚠ WARNING: Found 'Notes' in body text {len(matches)} time(s)")
                # Show context around "Notes"
                for match in re.finditer(notes_pattern, full_text, re.IGNORECASE):
                    start = max(0, match.start() - 50)
                    end = min(len(full_text), match.end() + 50)
                    context = full_text[start:end]
                    print(f"    Context: ...{context}...")
            else:
                print(f"  ✓ No 'Notes' header found in body text (good!)")

            talks_tested += 1
            if talks_tested >= 3:
                break
        else:
            print(f"  No footnotes in this talk")
    print()

print("\n✓ Test complete!")

