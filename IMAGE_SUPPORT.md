# Image Support in PDFs

## Overview

The PDF generator now includes images from General Conference talks in the generated PDFs. Images are automatically downloaded from the Church's servers and embedded at their proper locations within the talk content.

## What's Included

### Image Types
The following types of images are included in PDFs:
- **Portraits**: Photos of speakers and individuals mentioned in talks
- **Artwork**: Paintings, sculptures, and other religious artwork
- **Photographs**: Documentary photos and illustrations
- **Diagrams**: Visual aids used in presentations

### Image Features
- **Automatic Download**: Images are downloaded from churchofjesuschrist.org
- **Proper Positioning**: Images appear at their correct locations within the talk text
- **Captions**: Image titles and descriptions are included below each image
- **Scaling**: Images are automatically scaled to fit the page width while maintaining aspect ratio
- **Caching**: Downloaded images are cached to avoid redundant downloads

## Technical Details

### Dependencies
The image support requires the **Pillow** library (Python Imaging Library):
```bash
pip install Pillow
```

This is included in the `requirements.txt` file.

### How It Works

1. **HTML Parsing**: The `HTMLContentExtractor` class parses HTML content and identifies `<img>` tags
2. **Structured Content**: Content is stored as a sequence of text blocks and image references
3. **Image Download**: Images are downloaded from URLs using `urllib.request`
4. **Image Processing**: Pillow opens images to determine dimensions
5. **PDF Embedding**: ReportLab's `Image` flowable embeds images in the PDF
6. **Caption Generation**: Image titles/descriptions are added as captions

### Code Changes

#### conference_scraper.py
- **New Class**: `HTMLContentExtractor` replaces `HTMLTextExtractor`
  - Extracts both text and images from HTML
  - Preserves the order of content elements
  - Captures image metadata (URL, title, alt text, dimensions)

- **New Method**: `extract_content_from_html()`
  - Returns structured content with text and images
  - Maintains backward compatibility with text-only extraction

#### pdf_generator.py
- **New Imports**: Added `Image` from reportlab.platypus, `PIL.Image`, `urllib.request`, `io`
- **Image Cache**: Added `self.image_cache` to avoid re-downloading images
- **New Method**: `_download_image()` - Downloads images from URLs
- **New Method**: `_create_image_flowable()` - Creates ReportLab Image objects
- **Updated Method**: `_add_talk_to_story()` - Processes structured content with images

#### requirements.txt
- Added `Pillow>=10.0.0` for image processing

## Examples

### Talk with Images
When a talk includes images (like Elder Holland's "As a Little Child"), the PDF will include:
1. The talk title and speaker
2. Opening paragraphs
3. **Image 1**: Portrait of Easton Jolley (with caption)
4. More text content
5. **Image 2**: Easton in wheelchair (with caption)
6. Remaining text content

### Image Captions
Captions are formatted in italics, centered, with a smaller font size:
```
[Image appears here]
Portrait of Easton Jolley
```

## Testing

### Test Scripts
Two test scripts are provided:

1. **test_images.py**: Generates a PDF with the first 2 talks that contain images
   ```bash
   python test_images.py
   ```

2. **verify_images.py**: Shows the structured content of a single talk
   ```bash
   python verify_images.py
   ```

### Verification
To verify images are included:
1. Run `python test_images.py`
2. Open `Output/test_images.pdf`
3. Check that images appear within the talk content
4. Verify captions are present below images

## Performance

### Download Times
- Images are downloaded during PDF generation
- Typical image size: 50-200 KB
- Download time per image: 0.5-2 seconds
- Total additional time for a full conference: 1-3 minutes

### Caching
Images are cached in memory during PDF generation to avoid re-downloading if the same image appears multiple times.

## Troubleshooting

### Missing Images
If images don't appear in the PDF:
1. Check internet connection
2. Verify Pillow is installed: `pip list | grep -i pillow`
3. Check console output for download errors
4. Ensure image URLs are accessible

### Image Quality
Images are downloaded at a fixed width (500px) from the Church's image server. This provides good quality while keeping file sizes reasonable.

### Large PDF Files
PDFs with many images will be larger:
- Text-only conference: ~500 KB
- Conference with images: 5-15 MB (depending on number of images)

## Future Enhancements

Possible improvements for future versions:
- [ ] Configurable image quality/size
- [ ] Option to exclude images
- [ ] Progress bar for image downloads
- [ ] Parallel image downloading
- [ ] Local image caching between runs
- [ ] Support for image galleries/slideshows

## Notes

- Images are downloaded from `churchofjesuschrist.org/imgs/` domain
- Image URLs use the Church's IIIF image server
- Images are embedded directly in the PDF (not linked)
- The Church's copyright applies to all images

