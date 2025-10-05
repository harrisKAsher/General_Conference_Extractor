# Footnote Styling Guide

## Visual Appearance

### In-Text Footnote Markers
Footnote markers appear in the body text with the following styling:

- **Format**: Superscript numbers: ¹, ², ³, etc.
- **Color**: #166086 (blue)
- **Position**: Superscript (at the top of the line)
- **Font Size**: 7pt
- **Example**: `"Thy faith hath made thee whole."¹`

### Footnote List
At the end of each talk, under a "Notes" heading:

- **Format**: **1.** Footnote text here...
- **Number**: Bold
- **Font Size**: 9pt (smaller than body text)
- **Indentation**: Left indent for better organization

## Color Specification

**Footnote Marker Color**: `#166086`
- RGB: (22, 96, 134)
- A clear blue that's visible and professional
- Distinguishes footnotes from body text

## Implementation Details

### Two-Stage Processing

**Stage 1: Scraping (`conference_scraper.py`)**
- Footnote markers are temporarily stored as: `{{FOOTNOTE:1}}`
- This prevents them from being escaped during text cleaning

**Stage 2: PDF Generation (`pdf_generator.py`)**
- Markers are replaced with formatted HTML after text cleaning
- Final format: `<super><font color="#166086" size="7">1</font></super>`
- Uses `<super>` tag for superscript positioning
- Font size is 7pt for appropriate superscript sizing

### Why This Design?

1. **Superscript Position**: Traditional academic/publishing style, appears at top of line
2. **Blue Color (#166086)**:
   - Clearly distinguishes footnotes from body text
   - Professional and readable
   - Visible without being distracting
3. **Smaller Font (7pt)**: Appropriate size for superscript text
4. **No Brackets**: Clean, traditional superscript style
5. **Consistent Numbering**: Easy to match markers with footnotes at end of talk

## Customization

To change the color or size, edit `pdf_generator.py` in the `_clean_text_for_pdf` method:
```python
formatted_marker = f'<super><font color="#166086" size="7">{num}</font></super>'
```

**Color**: Replace `#166086` with your preferred hex color code
**Size**: Change `size="7"` to adjust font size (7pt is standard for superscript)
**Position**: Remove `<super>` tags to display inline instead of superscript
**Format**: Add brackets by changing `{num}` to `[{num}]`

