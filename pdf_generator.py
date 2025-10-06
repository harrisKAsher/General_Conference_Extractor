#!/usr/bin/env python3
"""
PDF Generator for General Conference Talks

This module generates formatted PDF documents from scraped conference data.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

A2 = (612,792) # A2 size in points (8.5x11 inches) US Letter
B5 = (498, 708) # B5 paper, I found this to work great digitally
PAGE_SIZE = A2
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, Frame, PageTemplate, Flowable
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfgen_canvas
import json
import sys
import re
import urllib.request
import io
from datetime import datetime
from typing import Dict, List, Optional
from PIL import Image as PILImage


class BookmarkFlowable(Flowable):
    """A flowable that adds a bookmark to the PDF outline"""

    def __init__(self, key, title, level=0):
        Flowable.__init__(self)
        self.key = key
        self.title = title
        self.level = level
        self.height = 0
        self.width = 0

    def draw(self):
        # Register the bookmark at the current position
        self.canv.bookmarkPage(self.key)
        self.canv.addOutlineEntry(self.title, self.key, self.level, closed=False)


class ConferencePDFGenerator:
    """Generates formatted PDF from conference data"""

    def __init__(self, conference_data: Dict):
        self.conference_data = conference_data
        self.styles = getSampleStyleSheet()
        self._register_unicode_fonts()
        self._setup_custom_styles()
        self.image_cache = {}  # Cache downloaded images
        self.conference_date = self._extract_conference_date()

    def _register_unicode_fonts(self):
        """Register Unicode-compatible fonts for supporting non-Latin characters"""
        try:
            # Try to register DejaVu Sans fonts (commonly available on most systems)
            # These fonts support a wide range of Unicode characters including Hebrew, Greek, etc.

            # Try common font paths for different operating systems
            font_paths = [
                # macOS
                '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
                '/Library/Fonts/Arial Unicode.ttf',
                # Linux
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
                '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf',
                # Windows
                'C:\\Windows\\Fonts\\Arial.ttf',
                'C:\\Windows\\Fonts\\Arialbd.ttf',
            ]

            # Try to register fonts
            fonts_registered = False

            # Try DejaVu Sans (Linux)
            try:
                pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
                pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
                pdfmetrics.registerFont(TTFont('DejaVuSerif', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))
                pdfmetrics.registerFont(TTFont('DejaVuSerif-Italic', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf'))
                self.font_regular = 'DejaVuSerif'
                self.font_bold = 'DejaVuSans-Bold'
                self.font_italic = 'DejaVuSerif-Italic'
                fonts_registered = True
                print("Using DejaVu fonts for Unicode support")
            except:
                pass

            # Try Arial Unicode (macOS)
            if not fonts_registered:
                try:
                    pdfmetrics.registerFont(TTFont('ArialUnicode', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
                    self.font_regular = 'ArialUnicode'
                    self.font_bold = 'ArialUnicode'
                    self.font_italic = 'ArialUnicode'
                    fonts_registered = True
                    print("Using Arial Unicode font for Unicode support")
                except:
                    pass

            # Fallback to standard fonts (won't support all Unicode)
            if not fonts_registered:
                print("Warning: Could not load Unicode fonts. Non-Latin characters may not display correctly.")
                self.font_regular = 'Times-Roman'
                self.font_bold = 'Helvetica-Bold'
                self.font_italic = 'Times-Italic'

        except Exception as e:
            print(f"Warning: Error registering fonts: {e}")
            # Fallback to standard fonts
            self.font_regular = 'Times-Roman'
            self.font_bold = 'Helvetica-Bold'
            self.font_italic = 'Times-Italic'

    def _extract_conference_date(self) -> str:
        """Extract conference date from conference title (e.g., 'April 2025')"""
        conference_title = self.conference_data.get('conference_title', '')

        # Try to extract month and year from title
        # Expected format: "April 2025 General Conference" or similar
        match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', conference_title)
        if match:
            return f"{match.group(1)} {match.group(2)}"

        # Fallback: try to get from first talk URL if available
        talks = self.conference_data.get('talks', [])
        if talks and 'url' in talks[0]:
            url = talks[0]['url']
            # URL format: .../general-conference/2025/04/...
            match = re.search(r'/general-conference/(\d{4})/(\d{2})/', url)
            if match:
                year = match.group(1)
                month_num = int(match.group(2))
                months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                         'July', 'August', 'September', 'October', 'November', 'December']
                if 1 <= month_num <= 12:
                    return f"{months[month_num]} {year}"

        return ""

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
            fontName=self.font_bold
        ))

        # Talk title style - larger and bolder
        self.styles.add(ParagraphStyle(
            name='TalkTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#003366'),
            spaceAfter=8,
            spaceBefore=0,
            alignment=TA_LEFT,
            fontName=self.font_bold
        ))

        # Speaker name style - with "By" prefix
        self.styles.add(ParagraphStyle(
            name='Speaker',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.black,
            spaceAfter=2,
            alignment=TA_LEFT,
            fontName=self.font_bold
        ))

        # Author role/title style
        self.styles.add(ParagraphStyle(
            name='AuthorRole',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.black,
            spaceAfter=2,
            alignment=TA_LEFT,
            fontName=self.font_italic
        ))

        # Conference date style
        self.styles.add(ParagraphStyle(
            name='ConferenceDate',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#5A7FA5'),
            spaceAfter=0,
            alignment=TA_LEFT,
            fontName=self.font_regular
        ))

        # Highlight/Lead paragraph style - first paragraph of talk
        self.styles.add(ParagraphStyle(
            name='TalkHighlight',
            parent=self.styles['Normal'],
            fontSize=14,
            leading=15,
            textColor=colors.HexColor('#486581'),
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            fontName=self.font_italic
        ))

        # Body text style
        self.styles.add(ParagraphStyle(
            name='TalkBody',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=12,
            alignment=TA_JUSTIFY,
            spaceAfter=5,
            fontName=self.font_regular
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
            fontName=self.font_bold
        ))

        # Footnote title style
        self.styles.add(ParagraphStyle(
            name='FootnoteTitle',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#003366'),
            spaceAfter=8,
            spaceBefore=0,
            alignment=TA_LEFT,
            fontName=self.font_bold
        ))

        # Footnote text style
        self.styles.add(ParagraphStyle(
            name='FootnoteText',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=11,
            alignment=TA_LEFT,
            spaceAfter=6,
            leftIndent=8,
            fontName=self.font_regular
        ))

        # Header styles for content headers (h2, h3, h4, etc.)
        # H2 - Main section headers
        self.styles.add(ParagraphStyle(
            name='ContentH2',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#003366'),
            spaceAfter=8,
            spaceBefore=16,
            alignment=TA_LEFT,
            fontName=self.font_bold
        ))

        # H3 - Subsection headers
        self.styles.add(ParagraphStyle(
            name='ContentH3',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#003366'),
            spaceAfter=6,
            spaceBefore=12,
            alignment=TA_LEFT,
            fontName=self.font_bold
        ))

        # H4 - Minor headers
        self.styles.add(ParagraphStyle(
            name='ContentH4',
            parent=self.styles['Heading3'],
            fontSize=11,
            textColor=colors.HexColor('#003366'),
            spaceAfter=5,
            spaceBefore=10,
            alignment=TA_LEFT,
            fontName=self.font_bold
        ))
        
    def _create_cover_page(self, story: List):
        """Create a cover page for the PDF with border and disclaimer"""
        # Add space from top to center content vertically
        story.append(Spacer(1, 2.5*inch))

        # Main title: "General Conference"
        title_style = ParagraphStyle(
            name='CoverTitle',
            parent=self.styles['Normal'],
            fontSize=36,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#003366'),
            fontName=self.font_bold,
            spaceAfter=36
        )
        title = Paragraph("General Conference", title_style)
        story.append(title)

        # Conference date (e.g., "April 2024")
        if self.conference_date:
            date_style = ParagraphStyle(
                name='CoverDate',
                parent=self.styles['Normal'],
                fontSize=24,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#003366'),
                fontName=self.font_regular
            )
            date_text = Paragraph(self.conference_date, date_style)
            story.append(date_text)

        # Add space to push disclaimer to bottom
        story.append(Spacer(1, 4.5*inch))

        # Very faint disclaimer at bottom
        disclaimer_style = ParagraphStyle(
            name='Disclaimer',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#E0E0E0'),  # Very light gray
            fontName=self.font_regular
        )
        disclaimer = Paragraph("This is not an official church production", disclaimer_style)
        story.append(disclaimer)

        # Page break after cover
        story.append(PageBreak())

    def _create_session_page(self, story: List, session_name: str, session_key: str):
        """Create a session header page"""
        # Add bookmark marker for this session (level 0 = top level)
        bookmark = BookmarkFlowable(session_key, session_name, level=0)
        story.append(bookmark)

        # Add some space from top
        story.append(Spacer(1, 3*inch))

        # Session title style
        session_title_style = ParagraphStyle(
            name='SessionTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#003366'),
            alignment=TA_CENTER,
            fontName=self.font_bold,
            spaceAfter=12
        )

        # Session title
        title = Paragraph(session_name, session_title_style)
        story.append(title)

        # Conference date below session title
        if self.conference_date:
            session_date_style = ParagraphStyle(
                name='SessionDate',
                parent=self.styles['Normal'],
                fontSize=16,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#5A7FA5'),
                fontName=self.font_regular
            )
            date_text = Paragraph(self.conference_date, session_date_style)
            story.append(date_text)

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
            '3': 'Sunday Evening Session',
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
        # First, temporarily replace footnote markers to protect them
        import re
        footnote_markers = {}
        footnote_pattern = r'\{\{FOOTNOTE:(\d+)\}\}'

        def save_footnote(match):
            num = match.group(1)
            marker_id = f"FOOTNOTE_PLACEHOLDER_{num}"
            footnote_markers[marker_id] = num
            return marker_id

        text = re.sub(footnote_pattern, save_footnote, text)

        # Replace special characters that might cause issues
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')

        # Handle non-breaking spaces
        text = text.replace('\xa0', ' ')

        # Now restore footnote markers with proper formatting
        for marker_id, num in footnote_markers.items():
            # Use ReportLab's super tag for superscript with color
            formatted_marker = f'<font size="1"> </font><super rise="3"><font color="#2D83AE" size="8">{num}</font></super>'
            text = text.replace(marker_id, formatted_marker)

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

    def _download_image(self, url: str) -> Optional[io.BytesIO]:
        """Download an image from a URL and return as BytesIO"""
        if url in self.image_cache:
            return self.image_cache[url]

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req, timeout=10) as response:
                image_data = response.read()
                image_buffer = io.BytesIO(image_data)
                self.image_cache[url] = image_buffer
                return image_buffer
        except Exception as e:
            print(f"    Warning: Failed to download image from {url}: {e}")
            return None

    def _create_image_flowable(self, image_info: Dict, max_width: float = None, max_height: float = None) -> Optional[Image]:
        """Create a ReportLab Image flowable from image info"""
        # Calculate max dimensions based on B5 page size with margins
        # The actual frame size is smaller due to internal padding in SimpleDocTemplate
        # Frame is 378.0 x 588.0 points, so we use slightly smaller values to be safe
        if max_width is None:
            max_width = 310  # Safe width within the 378 point frame
        if max_height is None:
            max_height = 310  # Safe height within the 588 point frame

        url = image_info.get('url', '')
        if not url:
            return None

        # Download the image
        image_buffer = self._download_image(url)
        if not image_buffer:
            return None

        try:
            # Reset buffer position
            image_buffer.seek(0)

            # Open with PIL to get dimensions
            pil_image = PILImage.open(image_buffer)
            img_width, img_height = pil_image.size

            # Calculate scaling to fit within max dimensions while maintaining aspect ratio
            width_scale = max_width / img_width if img_width > max_width else 1.0
            height_scale = max_height / img_height if img_height > max_height else 1.0
            scale = min(width_scale, height_scale)

            display_width = img_width * scale
            display_height = img_height * scale

            # Reset buffer for ReportLab
            image_buffer.seek(0)

            # Create ReportLab Image
            img = Image(image_buffer, width=display_width, height=display_height)

            return img
        except Exception as e:
            print(f"    Warning: Failed to process image: {e}")
            return None
        
    def _should_skip_paragraph(self, para_text: str, title: str, speaker: str, author_role: str = None) -> bool:
        """Check if a paragraph should be skipped (duplicate title/speaker info)"""
        para_clean = para_text.strip().lower()
        title_clean = title.strip().lower()
        speaker_clean = speaker.strip().lower()

        # Skip if paragraph matches title exactly
        if para_clean == title_clean:
            return True

        # Skip if paragraph matches speaker name (with or without "By")
        if para_clean == speaker_clean or para_clean == f"by {speaker_clean}":
            return True

        # Skip if paragraph starts with "By" and contains speaker name
        if para_clean.startswith("by ") and speaker_clean in para_clean:
            return True

        # Skip if paragraph matches the author role that was already displayed
        if author_role:
            author_role_clean = author_role.strip().lower()
            if para_clean == author_role_clean:
                return True

        # Skip common role/title lines that appear after speaker name
        role_keywords = [
            'president of the church',
            'first counselor in the first presidency',
            'second counselor in the first presidency',
            'acting president of the quorum of the twelve apostles',
            'president of the quorum of the twelve apostles',
            'of the quorum of the twelve apostles',
            'of the seventy',
            'first counselor in the',
            'second counselor in the',
            'presidency of the seventy',
            'general authority seventy',
            'young women general president',
            'young men general president',
            'primary general president',
            'relief society general president',
            'sunday school general president'
        ]

        for keyword in role_keywords:
            if keyword in para_clean:
                return True

        return False

    def _add_talk_to_story(self, story: List, talk: Dict, talk_number: int, parent_bookmark_key: str = None):
        """Add a single talk to the PDF story"""

        # Add bookmark marker for this talk (level 1 = nested under session)
        title = talk.get('title', 'Untitled')
        speaker = talk.get('speaker', 'Unknown')
        talk_key = f"talk_{talk_number}"
        bookmark_title = f"{speaker}: {title}"

        # Create bookmark as a child of the session (level 1)
        bookmark = BookmarkFlowable(talk_key, bookmark_title, level=1)
        story.append(bookmark)

        # Talk title
        title_para = Paragraph(self._clean_text_for_pdf(title), self.styles['TalkTitle'])
        story.append(title_para)

        # Speaker name with "By" prefix
        speaker_text = f"By {speaker}"
        speaker_para = Paragraph(self._clean_text_for_pdf(speaker_text), self.styles['Speaker'])
        story.append(speaker_para)

        # Author role/title (if available)
        author_role = talk.get('author_role')
        if author_role:
            role_para = Paragraph(self._clean_text_for_pdf(author_role), self.styles['AuthorRole'])
            story.append(role_para)

        # Conference date
        if self.conference_date:
            date_para = Paragraph(self.conference_date, self.styles['ConferenceDate'])
            story.append(date_para)

        story.append(Spacer(1, 0.15*inch))

        # Check if we have structured content (with images)
        structured_content = talk.get('structured_content', [])

        # Track if we've added the first paragraph (for highlight styling)
        first_paragraph_added = False

        if structured_content:
            # Use structured content to preserve image and header positions
            for item in structured_content:
                if item['type'] == 'text':
                    # Split text into paragraphs
                    paragraphs = self._split_into_paragraphs(item['content'])
                    for para_text in paragraphs:
                        if para_text:
                            # Skip duplicate title/speaker paragraphs
                            if self._should_skip_paragraph(para_text, title, speaker, author_role):
                                continue

                            cleaned_text = self._clean_text_for_pdf(para_text)
                            # Use highlight style for first paragraph, regular style for rest
                            if not first_paragraph_added:
                                para = Paragraph(cleaned_text, self.styles['TalkHighlight'])
                                first_paragraph_added = True
                            else:
                                para = Paragraph(cleaned_text, self.styles['TalkBody'])
                            story.append(para)

                elif item['type'] == 'header':
                    # Add header with appropriate style based on level
                    header_text = item.get('content', '')
                    header_level = item.get('level', 2)

                    # Skip if header matches the talk title (duplicate)
                    if header_text.strip().lower() == title.strip().lower():
                        continue

                    # Map header levels to styles (h1 is reserved for talk title)
                    # h2 -> ContentH2, h3 -> ContentH3, h4+ -> ContentH4
                    if header_level <= 2:
                        style_name = 'ContentH2'
                    elif header_level == 3:
                        style_name = 'ContentH3'
                    else:
                        style_name = 'ContentH4'

                    cleaned_text = self._clean_text_for_pdf(header_text)
                    header_para = Paragraph(cleaned_text, self.styles[style_name])
                    story.append(header_para)

                    # Mark that we've passed the first content (headers come after intro)
                    first_paragraph_added = True

                elif item['type'] == 'image':
                    # Add the image
                    img_flowable = self._create_image_flowable(item)
                    if img_flowable:
                        story.append(Spacer(1, 0.15*inch))
                        story.append(img_flowable)

                        # Add caption from credit field if available
                        caption = item.get('credit', '')
                        if caption:
                            caption_style = ParagraphStyle(
                                name='ImageCaption',
                                parent=self.styles['Normal'],
                                fontSize=9,
                                textColor=colors.HexColor('#666666'),
                                alignment=TA_CENTER,
                                spaceAfter=6,
                                spaceBefore=3,
                                fontName=self.font_italic
                            )
                            caption_para = Paragraph(self._clean_text_for_pdf(caption), caption_style)
                            story.append(caption_para)

                        story.append(Spacer(1, 0.15*inch))
        else:
            # Fallback to plain text content (for backward compatibility)
            content = talk.get('content', '')
            paragraphs = self._split_into_paragraphs(content)

            first_content_para = False
            for para_text in paragraphs:
                if para_text:
                    # Skip duplicate title/speaker paragraphs
                    if self._should_skip_paragraph(para_text, title, speaker, author_role):
                        continue

                    cleaned_text = self._clean_text_for_pdf(para_text)
                    # Use highlight style for first paragraph, regular style for rest
                    if not first_content_para:
                        para = Paragraph(cleaned_text, self.styles['TalkHighlight'])
                        first_content_para = True
                    else:
                        para = Paragraph(cleaned_text, self.styles['TalkBody'])
                    story.append(para)

        # Add footnotes if present
        footnotes = talk.get('footnotes', [])
        if footnotes:
            story.append(Spacer(1, 0.3*inch))

            # Footnotes title
            footnote_title = Paragraph("Notes", self.styles['FootnoteTitle'])
            story.append(footnote_title)

            # Add each footnote
            for footnote in footnotes:
                marker = footnote.get('marker', '').rstrip('.')  # Remove trailing period if present
                text = footnote.get('text', '')

                if marker and text:
                    # Clean the footnote text for PDF
                    cleaned_text = self._clean_text_for_pdf(text)
                    # Add the marker number at the beginning
                    footnote_para = Paragraph(f"<b>{marker}.</b> {cleaned_text}", self.styles['FootnoteText'])
                    story.append(footnote_para)

        # Page break after each talk
        story.append(PageBreak())
        
    def _draw_cover_border(self, canvas, doc):
        """Draw a decorative border on the cover page"""
        canvas.saveState()

        # Set border properties
        canvas.setStrokeColor(colors.HexColor('#003366'))
        canvas.setLineWidth(2)

        # Draw border with some margin from page edges
        margin = 0.5 * inch
        page_width, page_height = PAGE_SIZE

        canvas.rect(
            margin,
            margin,
            page_width - 2*margin,
            page_height - 2*margin,
            stroke=1,
            fill=0
        )

        canvas.restoreState()

    def _on_first_page(self, canvas, doc):
        """Callback for the first page (cover page) with border"""
        self._draw_cover_border(canvas, doc)

    def _on_later_pages(self, canvas, doc):
        """Callback for pages after the cover (no border)"""
        pass

    def generate_pdf(self, output_filename: str):
        """Generate the PDF document"""

        print(f"\nGenerating PDF: {output_filename}")
        print("="*80)

        # Create the PDF document with custom page templates
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=PAGE_SIZE,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )

        # Build the story (content)
        story = []

        # Add cover page
        print("\nAdding cover page...")
        self._create_cover_page(story)

        # Add each talk with session headers
        talks = self.conference_data.get('talks', [])
        print(f"\nAdding {len(talks)} talks to PDF...")

        current_session = None
        current_session_key = None
        for i, talk in enumerate(talks, 1):
            speaker = talk.get('speaker', 'Unknown')
            title = talk.get('title', 'Untitled')
            talk_url = talk.get('url', '')

            # Check if we're starting a new session
            session_number = self._extract_session_number(talk_url)
            if session_number != current_session and session_number != '0':
                current_session = session_number
                session_name = self._get_session_name(session_number)
                current_session_key = f"session_{session_number}"
                print(f"\n  === {session_name} ===")
                self._create_session_page(story, session_name, current_session_key)

            print(f"  [{i}/{len(talks)}] {speaker}: {title}")
            self._add_talk_to_story(story, talk, i, current_session_key)

        # Build the PDF with custom page callbacks
        print("\nBuilding PDF document...")
        doc.build(story, onFirstPage=self._on_first_page, onLaterPages=self._on_later_pages)

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

