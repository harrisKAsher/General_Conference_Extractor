#!/usr/bin/env python3
"""
General Conference Scraper and PDF Generator

This script scrapes talks from Church of Jesus Christ General Conference pages
and generates formatted PDF documents.

Usage:
    python conference_scraper.py <conference_url>
    
Example:
    python conference_scraper.py https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng
"""

import sys
import re
import json
import urllib.request
from html.parser import HTMLParser
from typing import List, Dict, Optional
from datetime import datetime
from html import unescape


def strip_html_tags(html_text: str) -> str:
    """Strip HTML tags from text while preserving content"""
    # Remove HTML tags but keep the text content
    text = re.sub(r'<[^>]+>', '', html_text)
    # Unescape HTML entities
    text = unescape(text)
    # Clean up whitespace
    text = ' '.join(text.split())
    return text


class HTMLContentExtractor(HTMLParser):
    """Extract text content and images from HTML while preserving structure"""

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.content_parts = []  # List of tuples: ('text', content) or ('image', image_info)
        self.current_text = []
        self.in_paragraph = False
        self.in_header = False
        self.in_emphasis = False
        self.in_footer = False  # Track if we're in the footnotes section
        self.footnotes = []  # List of footnote dictionaries
        self.current_footnote = None  # Current footnote being parsed
        self.in_footnote_text = False  # Track if we're in footnote text

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Check if we're entering the footnotes section
        if tag == 'footer':
            self.in_footer = True
            # Save any accumulated text before footnotes
            if self.current_text:
                text = ''.join(self.current_text).strip()
                if text:
                    self.content_parts.append(('text', text))
                self.current_text = []
            return

        # Skip processing if we're in the footer (footnotes section)
        if self.in_footer:
            if tag == 'li' and 'data-marker' in attrs_dict:
                # Start a new footnote
                self.current_footnote = {
                    'marker': attrs_dict.get('data-marker', ''),
                    'id': attrs_dict.get('id', ''),
                    'text': []
                }
                self.in_footnote_text = True
            return

        # Handle superscript footnote markers in the text
        if tag == 'sup' and attrs_dict.get('class') == 'marker':
            footnote_num = attrs_dict.get('data-value', '')
            if footnote_num:
                # Use a special marker that won't be escaped
                # We'll replace this in the PDF generator
                self.current_text.append(f'{{{{FOOTNOTE:{footnote_num}}}}}')
            return

        if tag == 'p':
            self.in_paragraph = True
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_header = True
        elif tag in ['em', 'i', 'strong', 'b']:
            self.in_emphasis = True
        elif tag == 'br':
            self.current_text.append('\n')
        elif tag == 'img':
            # Save any accumulated text first
            if self.current_text:
                text = ''.join(self.current_text).strip()
                if text:
                    self.content_parts.append(('text', text))
                self.current_text = []

            # Extract image information
            image_info = {
                'src': attrs_dict.get('src', ''),
                'alt': attrs_dict.get('alt', ''),
                'data-public-title': attrs_dict.get('data-public-title', ''),
                'data-public-description': attrs_dict.get('data-public-description', ''),
                'data-width': attrs_dict.get('data-width', ''),
                'data-height': attrs_dict.get('data-height', '')
            }
            self.content_parts.append(('image', image_info))

    def handle_endtag(self, tag):
        if tag == 'footer':
            self.in_footer = False
            return

        # Handle footnote list items
        if self.in_footer:
            if tag == 'li' and self.current_footnote:
                # Finish current footnote
                footnote_text = ''.join(self.current_footnote['text']).strip()
                self.current_footnote['text'] = footnote_text
                self.footnotes.append(self.current_footnote)
                self.current_footnote = None
                self.in_footnote_text = False
            return

        if tag == 'p':
            self.in_paragraph = False
            self.current_text.append('\n\n')
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_header = False
            self.current_text.append('\n\n')
        elif tag in ['em', 'i', 'strong', 'b']:
            self.in_emphasis = False

    def handle_data(self, data):
        if self.in_footer and self.in_footnote_text and self.current_footnote:
            # Accumulate footnote text
            self.current_footnote['text'].append(data)
        elif data.strip():
            self.current_text.append(data)

    def get_content(self):
        """Return list of content parts (text and images) and footnotes"""
        # Add any remaining text
        if self.current_text:
            text = ''.join(self.current_text).strip()
            if text:
                self.content_parts.append(('text', text))
        return self.content_parts, self.footnotes


class ConferenceScraper:
    """Scrapes General Conference talks from churchofjesuschrist.org"""
    
    BASE_URL = "https://www.churchofjesuschrist.org"
    API_BASE = "https://www.churchofjesuschrist.org/study/api/v3/language-pages/type/content"
    
    def __init__(self, conference_url: str):
        self.conference_url = conference_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
    def extract_uri_from_url(self, url: str) -> str:
        """Extract the URI path from a full URL"""
        # Remove base URL and query parameters
        uri = url.replace(self.BASE_URL, '')
        uri = uri.split('?')[0]

        # Remove /study prefix if present (API doesn't need it)
        if uri.startswith('/study'):
            uri = uri[6:]  # Remove '/study'

        return uri
        
    def fetch_conference_data(self) -> Dict:
        """Fetch the main conference page data"""
        uri = self.extract_uri_from_url(self.conference_url)
        api_url = f"{self.API_BASE}?lang=eng&uri={uri}"
        
        print(f"Fetching conference data from: {api_url}")
        req = urllib.request.Request(api_url, headers=self.headers)
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
            
    def parse_talk_links(self, html_body: str) -> List[Dict[str, str]]:
        """Parse talk links, speakers, and titles from the conference page HTML"""
        talks = []

        # Extract all talk entries - look for <li> tags with data-content-type
        # First, find all talk/business items
        talk_items = re.findall(
            r'<li[^>]*data-content-type="(general-conference-talk|general-conference-business)"[^>]*>(.*?)</li>',
            html_body,
            re.DOTALL
        )

        for content_type, item_html in talk_items:
            # Extract URL
            url_match = re.search(r'href="([^"]+)"', item_html)
            if not url_match:
                continue
            url = url_match.group(1).split('?')[0]

            # Skip session overviews
            if 'session' in url:
                continue

            # Extract speaker (primaryMeta)
            speaker_match = re.search(r'<p class="primaryMeta">([^<]+)</p>', item_html)
            speaker = speaker_match.group(1).strip() if speaker_match else 'Unknown'

            # Extract title
            title_match = re.search(r'<p class="title">([^<]+)</p>', item_html)
            title = title_match.group(1).strip() if title_match else 'Untitled'

            # Skip sustaining and audit reports
            title_lower = title.lower()
            if 'sustaining' in title_lower or 'audit' in title_lower:
                continue

            talk_info = {
                'url': url,
                'speaker': speaker,
                'title': title,
                'type': content_type
            }
            talks.append(talk_info)

        return talks
        
    def fetch_talk_content(self, talk_url: str) -> Optional[Dict]:
        """Fetch the full content of a single talk"""
        # Remove /study prefix if present
        uri = talk_url
        if uri.startswith('/study'):
            uri = uri[6:]

        api_url = f"{self.API_BASE}?lang=eng&uri={uri}"

        print(f"  Fetching: {uri}")
        req = urllib.request.Request(api_url, headers=self.headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data
        except Exception as e:
            print(f"  Error fetching {talk_url}: {e}")
            return None
            
    def extract_content_from_html(self, html: str) -> Dict:
        """Extract text and images from HTML content"""
        # First, extract footnotes using regex (more reliable for nested HTML)
        footnotes = []
        footnote_pattern = r'<li[^>]*data-marker="([^"]+)"[^>]*id="([^"]+)"[^>]*>(.*?)</li>'
        for match in re.finditer(footnote_pattern, html, re.DOTALL):
            marker = match.group(1)
            note_id = match.group(2)
            footnote_html = match.group(3)

            # Strip HTML tags from footnote text
            footnote_text = strip_html_tags(footnote_html)

            footnotes.append({
                'marker': marker,
                'id': note_id,
                'text': footnote_text
            })

        # Now extract content (text and images)
        extractor = HTMLContentExtractor()
        extractor.feed(html)
        content_parts, _ = extractor.get_content()  # Ignore footnotes from extractor

        # Build structured content with images at their proper positions
        structured_content = []

        for content_type, content in content_parts:
            if content_type == 'text':
                structured_content.append({
                    'type': 'text',
                    'content': content
                })
            elif content_type == 'image':
                structured_content.append({
                    'type': 'image',
                    'url': content['src'],
                    'alt': content['alt'],
                    'title': content['data-public-title'],
                    'description': content['data-public-description'],
                    'width': content['data-width'],
                    'height': content['data-height']
                })

        # For backward compatibility, also provide text-only version
        text_parts = [item['content'] for item in structured_content if item['type'] == 'text']

        return {
            'text': '\n\n'.join(text_parts),
            'structured_content': structured_content,
            'footnotes': footnotes
        }
        
    def scrape_all_talks(self) -> List[Dict]:
        """Scrape all talks from the conference"""
        # Get conference page
        conference_data = self.fetch_conference_data()
        
        # Extract conference title and metadata
        conference_title = conference_data['meta'].get('title', 'General Conference')
        print(f"\nConference: {conference_title}")
        print("="*80)
        
        # Parse talk links
        html_body = conference_data['content']['body']
        talk_links = self.parse_talk_links(html_body)
        
        print(f"\nFound {len(talk_links)} talks to scrape")
        print("="*80)
        
        # Fetch each talk's content
        talks = []
        for i, talk_info in enumerate(talk_links, 1):
            print(f"\n[{i}/{len(talk_links)}] {talk_info['speaker']}: {talk_info['title']}")

            talk_data = self.fetch_talk_content(talk_info['url'])
            if talk_data:
                # Extract text content and images
                body_html = talk_data['content']['body']
                content_data = self.extract_content_from_html(body_html)

                talk_info['content'] = content_data['text']
                talk_info['structured_content'] = content_data['structured_content']
                talk_info['footnotes'] = content_data.get('footnotes', [])
                talk_info['full_data'] = talk_data

                # Count images and footnotes
                image_count = sum(1 for item in content_data['structured_content'] if item['type'] == 'image')
                footnote_count = len(content_data.get('footnotes', []))
                if image_count > 0:
                    print(f"  Found {image_count} image(s)")
                if footnote_count > 0:
                    print(f"  Found {footnote_count} footnote(s)")

                talks.append(talk_info)
                
        return {
            'conference_title': conference_title,
            'talks': talks,
            'scraped_at': datetime.now().isoformat()
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python conference_scraper.py <conference_url>")
        print("\nExample:")
        print("  python conference_scraper.py https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng")
        sys.exit(1)
        
    conference_url = sys.argv[1]
    
    # Scrape the conference
    scraper = ConferenceScraper(conference_url)
    conference_data = scraper.scrape_all_talks()
    
    # Save to JSON file
    output_filename = f"conference_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(conference_data, f, indent=2, ensure_ascii=False)
        
    print(f"\n{'='*80}")
    print(f"Scraping complete!")
    print(f"Data saved to: {output_filename}")
    print(f"Total talks scraped: {len(conference_data['talks'])}")
    print(f"{'='*80}")
    
    return conference_data


if __name__ == '__main__':
    main()

