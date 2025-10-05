#!/usr/bin/env python3
"""
PDF Generator for General Conference Talks

This module generates formatted PDF documents from scraped conference data.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json
import sys
import re
from datetime import datetime
from typing import Dict, List


class ConferencePDFGenerator:
    """Generates formatted PDF from conference data"""
    
    def __init__(self, conference_data: Dict):
        self.conference_data = conference_data
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the PDF"""
        
        # Title style for conference title
        self.styles.add(ParagraphStyle(
            name='ConferenceTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#003366'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Talk title style
        self.styles.add(ParagraphStyle(
            name='TalkTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#003366'),
            spaceAfter=6,
            spaceBefore=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Speaker name style
        self.styles.add(ParagraphStyle(
            name='Speaker',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#666666'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='TalkBody',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            fontName='Helvetica'
        ))
        
        # Session header style
        self.styles.add(ParagraphStyle(
            name='SessionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#003366'),
            spaceAfter=12,
            spaceBefore=20,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        ))
        
    def _create_cover_page(self, story: List):
        """Create a cover page for the PDF"""
        conference_title = self.conference_data.get('conference_title', 'General Conference')

        # Add some space from top
        story.append(Spacer(1, 2*inch))

        # Conference title
        title = Paragraph(conference_title, self.styles['ConferenceTitle'])
        story.append(title)
        story.append(Spacer(1, 0.5*inch))

        # Subtitle
        subtitle_style = ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666')
        )
        subtitle = Paragraph(
            "The Church of Jesus Christ of Latter-day Saints",
            subtitle_style
        )
        story.append(subtitle)
        story.append(Spacer(1, 0.3*inch))

        # Generated date
        date_style = ParagraphStyle(
            name='DateStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#999999')
        )
        date_text = Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            date_style
        )
        story.append(date_text)

        # Page break after cover
        story.append(PageBreak())

    def _create_session_page(self, story: List, session_name: str):
        """Create a session header page"""
        # Add some space from top
        story.append(Spacer(1, 3*inch))

        # Session title style
        session_title_style = ParagraphStyle(
            name='SessionTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#003366'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        # Session title
        title = Paragraph(session_name, session_title_style)
        story.append(title)

        # Page break after session header
        story.append(PageBreak())

    def _extract_session_number(self, talk_url: str) -> str:
        """Extract session number from talk URL"""
        # URLs are like /study/general-conference/2025/04/13holland
        # The first digit of the number indicates the session (1=Sat AM, 2=Sat PM, etc.)
        match = re.search(r'/(\d+)[a-z]', talk_url)
        if match:
            full_number = match.group(1)
            return full_number[0]  # Return first digit as session number
        return '0'

    def _get_session_name(self, session_number: str) -> str:
        """Map session number to session name"""
        session_names = {
            '1': 'Saturday Morning Session',
            '2': 'Saturday Afternoon Session',
            '3': 'Priesthood Session',
            '4': 'Sunday Morning Session',
            '5': 'Sunday Afternoon Session'
        }
        return session_names.get(session_number, f'Session {session_number}')
        
    def _create_table_of_contents(self, story: List):
        """Create a table of contents"""
        toc_title = Paragraph("Table of Contents", self.styles['ConferenceTitle'])
        story.append(toc_title)
        story.append(Spacer(1, 0.3*inch))
        
        # Create TOC entries
        toc_style = ParagraphStyle(
            name='TOCEntry',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=16,
            leftIndent=20
        )
        
        for i, talk in enumerate(self.conference_data['talks'], 1):
            speaker = talk.get('speaker', 'Unknown')
            title = talk.get('title', 'Untitled')
            
            toc_entry = f"{i}. <b>{title}</b> - {speaker}"
            story.append(Paragraph(toc_entry, toc_style))
            story.append(Spacer(1, 6))
            
        story.append(PageBreak())
        
    def _clean_text_for_pdf(self, text: str) -> str:
        """Clean and prepare text for PDF rendering"""
        # Replace special characters that might cause issues
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        
        # Handle non-breaking spaces
        text = text.replace('\xa0', ' ')
        
        return text
        
    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        # Split by double newlines
        paragraphs = text.split('\n\n')
        
        # Clean up each paragraph
        cleaned = []
        for para in paragraphs:
            para = para.strip()
            if para:
                # Replace single newlines with spaces
                para = para.replace('\n', ' ')
                # Remove extra spaces
                para = ' '.join(para.split())
                cleaned.append(para)
                
        return cleaned
        
    def _add_talk_to_story(self, story: List, talk: Dict, talk_number: int):
        """Add a single talk to the PDF story"""
        
        # Talk title
        title = talk.get('title', 'Untitled')
        title_para = Paragraph(self._clean_text_for_pdf(title), self.styles['TalkTitle'])
        story.append(title_para)
        
        # Speaker name
        speaker = talk.get('speaker', 'Unknown')
        speaker_para = Paragraph(self._clean_text_for_pdf(speaker), self.styles['Speaker'])
        story.append(speaker_para)
        
        story.append(Spacer(1, 0.2*inch))
        
        # Talk content
        content = talk.get('content', '')
        paragraphs = self._split_into_paragraphs(content)
        
        for para_text in paragraphs:
            if para_text:
                cleaned_text = self._clean_text_for_pdf(para_text)
                para = Paragraph(cleaned_text, self.styles['TalkBody'])
                story.append(para)
                
        # Page break after each talk
        story.append(PageBreak())
        
    def generate_pdf(self, output_filename: str):
        """Generate the PDF document"""
        
        print(f"\nGenerating PDF: {output_filename}")
        print("="*80)
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build the story (content)
        story = []

        # Add each talk with session headers
        talks = self.conference_data.get('talks', [])
        print(f"\nAdding {len(talks)} talks to PDF...")

        current_session = None
        for i, talk in enumerate(talks, 1):
            speaker = talk.get('speaker', 'Unknown')
            title = talk.get('title', 'Untitled')
            talk_url = talk.get('url', '')

            # Check if we're starting a new session
            session_number = self._extract_session_number(talk_url)
            if session_number != current_session and session_number != '0':
                current_session = session_number
                session_name = self._get_session_name(session_number)
                print(f"\n  === {session_name} ===")
                self._create_session_page(story, session_name)

            print(f"  [{i}/{len(talks)}] {speaker}: {title}")
            self._add_talk_to_story(story, talk, i)
            
        # Build the PDF
        print("\nBuilding PDF document...")
        doc.build(story)
        
        print(f"\n{'='*80}")
        print(f"PDF generated successfully: {output_filename}")
        print(f"{'='*80}")


def main():
    """Main function for standalone PDF generation from JSON"""
    if len(sys.argv) < 2:
        print("Usage: python pdf_generator.py <conference_data.json> [output.pdf]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "conference_output.pdf"
    
    # Load conference data
    print(f"Loading conference data from: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        conference_data = json.load(f)
        
    # Generate PDF
    generator = ConferencePDFGenerator(conference_data)
    generator.generate_pdf(output_file)


if __name__ == '__main__':
    main()

