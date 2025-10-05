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


class HTMLTextExtractor(HTMLParser):
    """Extract text content from HTML while preserving some structure"""
    
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text_parts = []
        self.in_paragraph = False
        self.in_header = False
        self.in_emphasis = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.in_paragraph = True
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_header = True
        elif tag in ['em', 'i', 'strong', 'b']:
            self.in_emphasis = True
        elif tag == 'br':
            self.text_parts.append('\n')
            
    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_paragraph = False
            self.text_parts.append('\n\n')
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_header = False
            self.text_parts.append('\n\n')
        elif tag in ['em', 'i', 'strong', 'b']:
            self.in_emphasis = False
            
    def handle_data(self, data):
        if data.strip():
            self.text_parts.append(data)
            
    def get_text(self):
        return ''.join(self.text_parts).strip()


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
            
    def extract_text_from_html(self, html: str) -> str:
        """Extract clean text from HTML content"""
        extractor = HTMLTextExtractor()
        extractor.feed(html)
        return extractor.get_text()
        
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
                # Extract text content
                body_html = talk_data['content']['body']
                text_content = self.extract_text_from_html(body_html)
                
                talk_info['content'] = text_content
                talk_info['full_data'] = talk_data
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

