# Footnotes Feature

## Overview
Footnotes are now automatically extracted from conference talks and displayed with numbers both in the text and in the footnote list at the end of each talk.

## What Changed

### 1. Footnote Extraction (`conference_scraper.py`)
- **Footnote Markers in Text**: Superscript footnote markers (`<sup class="marker" data-value="1">`) are now converted to bracketed numbers like `[1]`, `[2]`, etc. in the text
- **Footnote List**: The footnote list at the bottom of each talk is extracted with:
  - Marker number (e.g., "1.", "2.")
  - Full footnote text (with HTML tags stripped)
  - Footnote ID for reference

### 2. PDF Generation (`pdf_generator.py`)
- **New Styles Added**:
  - `FootnoteTitle`: Bold heading for "Notes" section
  - `FootnoteText`: Smaller font (9pt) for footnote content with left indent
  
- **Footnote Display**: At the end of each talk, before the page break:
  - "Notes" heading is displayed
  - Each footnote shows as: **1.** Footnote text here...
  - Numbers are bold for easy reference

## Example

### In the Text:
```
And the Savior said to him who was thankful, "Thy faith hath made thee whole."[1]
```

### In the Footnotes Section:
```
Notes

1. See Luke 17:11–19. The term "made whole" was translated from a Greek word 
   that means to save, to rescue, to deliver, or to heal.

2. See Alma 40:23: "The soul shall be restored to the body, and the body to 
   the soul; yea, and every limb and joint shall be restored to its body..."
```

## Technical Details

### HTML Structure
Conference talks on churchofjesuschrist.org use this structure:
- **In-text markers**: `<sup class="marker" data-value="1"></sup>`
- **Footnote list**: `<footer><ol><li data-marker="1." id="note1">...</li></ol></footer>`

### Extraction Process
1. Regex pattern matches footnote `<li>` elements in the HTML
2. HTML tags within footnotes are stripped using `strip_html_tags()` function
3. Footnote markers in text are replaced with `[number]` format
4. Footnotes are stored in the talk data structure

### PDF Rendering
1. Talk content is rendered with footnote markers visible as `[1]`, `[2]`, etc.
2. After all talk content, a "Notes" section is added
3. Each footnote is rendered with its number in bold followed by the text
4. Footnotes use smaller font (9pt) and left indentation for readability

## Files Modified
- `conference_scraper.py`: Added footnote extraction logic
- `pdf_generator.py`: Added footnote styles and rendering
- Both files work together to preserve footnote information from scraping through to PDF generation

## Testing
Run these test scripts to verify footnote functionality:
- `test_footnote_extraction.py`: Verify footnotes are extracted from HTML
- `verify_footnotes.py`: Check footnote markers in text and list
- `test_single_talk_pdf.py`: Generate a single-talk PDF to inspect footnotes

## Benefits
- **Complete Information**: All scripture references and notes are preserved
- **Easy Reference**: Numbered markers make it easy to find corresponding footnotes
- **Professional Format**: Matches the style of published conference materials
- **Automatic**: No manual work needed - footnotes are extracted and formatted automatically

