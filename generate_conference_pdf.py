#!/usr/bin/env python3
"""
Complete General Conference PDF Generator

This script combines web scraping and PDF generation to create formatted
PDF documents from General Conference talks.

Usage:
    python generate_conference_pdf.py <conference_url> [output_pdf]
    
Example:
    python generate_conference_pdf.py https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng 2025_April.pdf
"""

import sys
import os
import json
from datetime import datetime
from conference_scraper import ConferenceScraper
from pdf_generator import ConferencePDFGenerator


def extract_conference_name(url: str) -> str:
    """Extract a readable conference name from the URL"""
    # Extract year and month from URL
    # Example: /general-conference/2025/04 -> 2025_April
    import re
    match = re.search(r'/general-conference/(\d{4})/(\d{2})', url)
    if match:
        year = match.group(1)
        month_num = match.group(2)
        
        # Convert month number to name
        months = {
            '04': 'April',
            '10': 'October'
        }
        month_name = months.get(month_num, month_num)
        
        return f"{year}_{month_name}"
    
    return f"conference_{datetime.now().strftime('%Y%m%d')}"


def main():
    """Main function"""

    print("="*80)
    print("General Conference PDF Generator")
    print("="*80)

    # Parse arguments
    if len(sys.argv) < 2:
        print("\nUsage: python generate_conference_pdf.py <conference_url> [output_pdf]")
        print("\nExample:")
        print("  python generate_conference_pdf.py https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng")
        print("  python generate_conference_pdf.py https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng 2025_April.pdf")
        sys.exit(1)

    conference_url = sys.argv[1]

    # Create Output directory if it doesn't exist
    output_dir = "Output"
    os.makedirs(output_dir, exist_ok=True)

    # Determine output filename
    if len(sys.argv) > 2:
        output_pdf = sys.argv[2]
        # If user provided a filename without directory, put it in Output
        if not os.path.dirname(output_pdf):
            output_pdf = os.path.join(output_dir, output_pdf)
    else:
        conference_name = extract_conference_name(conference_url)
        output_pdf = os.path.join(output_dir, f"{conference_name}.pdf")

    print(f"\nConference URL: {conference_url}")
    print(f"Output PDF: {output_pdf}")
    print()
    
    # Step 1: Scrape the conference
    print("\n" + "="*80)
    print("STEP 1: Scraping Conference Data")
    print("="*80)

    scraper = ConferenceScraper(conference_url)
    conference_data = scraper.scrape_all_talks()

    # Step 2: Generate PDF
    print("\n" + "="*80)
    print("STEP 2: Generating PDF")
    print("="*80)
    
    generator = ConferencePDFGenerator(conference_data)
    generator.generate_pdf(output_pdf)
    
    # Summary
    print("\n" + "="*80)
    print("COMPLETE!")
    print("="*80)
    print(f"\nConference: {conference_data['conference_title']}")
    print(f"Total talks: {len(conference_data['talks'])}")
    print(f"\nOutput file:")
    print(f"  - PDF: {output_pdf}")
    print("\n" + "="*80)


if __name__ == '__main__':
    main()

