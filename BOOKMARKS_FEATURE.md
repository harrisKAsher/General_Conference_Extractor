# PDF Bookmarks/Outline Feature

## Overview

The PDF generator now automatically creates a hierarchical bookmark structure (also called an "outline" or "table of contents") that allows PDF readers to display a navigable sidebar for jumping between sections and talks.

## What Are PDF Bookmarks?

PDF bookmarks (also known as outlines) are a navigation feature built into PDF files that:
- Appear in a sidebar panel in most PDF readers (Adobe Acrobat, Preview, Chrome, etc.)
- Allow users to quickly jump to different sections of the document
- Can be hierarchical (nested) to show document structure
- Are separate from the visual table of contents in the document

## How It Works

The PDF generator automatically creates bookmarks for:

### Level 0 (Top Level) - Sessions
Each conference session gets a top-level bookmark:
- Saturday Morning Session
- Saturday Afternoon Session  
- Priesthood Session
- Sunday Morning Session
- Sunday Afternoon Session

### Level 1 (Nested) - Individual Talks
Each talk is nested under its session with the format:
- `Speaker Name: Talk Title`

For example:
```
📖 Saturday Morning Session
  └─ Russell M. Nelson: The Lord Jesus Christ Will Come Again
  └─ Dallin H. Oaks: The Savior's Teachings about Prayer
📖 Saturday Afternoon Session
  └─ Henry B. Eyring: Witnesses for God
  └─ ...
```

## Viewing Bookmarks

### In Adobe Acrobat Reader
1. Open the PDF
2. Click the bookmark icon in the left sidebar (looks like a ribbon)
3. The outline tree will appear showing all sessions and talks

### In macOS Preview
1. Open the PDF
2. Click View → Sidebar (or press ⌘⌥3)
3. Click the "Table of Contents" tab in the sidebar

### In Chrome/Edge
1. Open the PDF
2. Click the bookmark icon in the toolbar
3. The outline will appear in a sidebar

### In Firefox
1. Open the PDF
2. Click the document outline icon (three horizontal lines with dots)
3. The outline will appear in a sidebar

## Technical Implementation

The feature uses ReportLab's bookmark and outline functionality:

1. **BookmarkFlowable Class**: A custom Flowable that adds bookmarks at specific positions in the document
2. **bookmarkPage()**: Registers a destination that can be jumped to
3. **addOutlineEntry()**: Adds an entry to the PDF's outline tree with a title, key, and hierarchy level

### Code Example

```python
# Create a bookmark for a session (level 0)
bookmark = BookmarkFlowable("session_1", "Saturday Morning Session", level=0)
story.append(bookmark)

# Create a bookmark for a talk (level 1, nested under session)
bookmark = BookmarkFlowable("talk_1", "Russell M. Nelson: The Lord Jesus Christ Will Come Again", level=1)
story.append(bookmark)
```

## Benefits

1. **Improved Navigation**: Users can quickly jump to any talk without scrolling
2. **Better User Experience**: Especially helpful for long documents with many talks
3. **Professional Appearance**: Matches the quality of official PDF publications
4. **Accessibility**: Screen readers can use bookmarks for navigation
5. **No Visual Impact**: Bookmarks don't affect the printed or visual appearance of the PDF

## Verification

To verify that bookmarks are present in a PDF, use the included verification script:

```bash
python verify_bookmarks.py your_conference.pdf
```

This will display the complete bookmark structure found in the PDF.

## Compatibility

PDF bookmarks are part of the PDF specification and are supported by:
- ✅ Adobe Acrobat Reader (all versions)
- ✅ macOS Preview
- ✅ Chrome/Chromium PDF viewer
- ✅ Firefox PDF viewer
- ✅ Microsoft Edge PDF viewer
- ✅ Most mobile PDF readers (iOS, Android)
- ✅ E-readers that support PDF

## Future Enhancements

Possible future improvements:
- Add bookmarks for the cover page and table of contents
- Add bookmarks for footnotes sections
- Allow customization of bookmark titles
- Support for deeper nesting levels (e.g., subsections within talks)

