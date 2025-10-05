# General Conference PDF Generator

A Python web scraping tool that extracts talks from Church of Jesus Christ General Conference pages and generates formatted PDF documents.

## Features

- Scrapes conference talks from churchofjesuschrist.org
- Extracts speaker names, talk titles, and full content
- Generates professionally formatted PDF documents
- Includes cover page and table of contents
- Reusable for different conference years and sessions
- Saves intermediate JSON data for debugging

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Quick Setup (Recommended)

Run the setup script to automatically create a virtual environment and install dependencies:

```bash
./setup.sh
```

Then activate the virtual environment:

```bash
source venv/bin/activate
```

### Manual Setup

If you prefer to set up manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Or install the package directly:

```bash
pip install reportlab
```

## Usage

**Important:** Make sure to activate the virtual environment before running the scripts:

```bash
source venv/bin/activate
```

### Quick Start

Generate a PDF from a conference URL (note the quotes around the URL):

```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"
```

**Important:** Always wrap the URL in quotes to prevent shell expansion issues.

This will create a PDF file named `2025_April.pdf` in the current directory.

### Specify Output Filename

```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng" my_conference.pdf
```

### Advanced Usage

#### Scrape Only (No PDF)

To scrape conference data and save as JSON without generating a PDF:

```bash
python conference_scraper.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"
```

This creates a JSON file with all scraped data.

#### Generate PDF from Existing JSON

If you already have scraped data in JSON format:

```bash
python pdf_generator.py conference_data.json output.pdf
```

## File Structure

```
.
├── generate_conference_pdf.py  # Main script (scrape + generate PDF)
├── conference_scraper.py       # Web scraping module
├── pdf_generator.py            # PDF generation module
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── example/
    └── 2025_April.pdf         # Example output
```

## How It Works

1. **Web Scraping**: The script uses the Church's API to fetch conference data
   - Retrieves the main conference page
   - Extracts links to individual talks
   - Fetches full content for each talk
   - Parses HTML to extract clean text

2. **PDF Generation**: Creates a formatted PDF using ReportLab
   - Cover page with conference title
   - Table of contents with all talks
   - Individual pages for each talk with speaker and title
   - Professional formatting and styling

## Examples

### April 2025 General Conference

```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"
```

### October 2024 General Conference

```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2024/10?lang=eng"
```

## Output

The script generates two files:

1. **PDF File**: Formatted document with all talks
   - Example: `2025_April.pdf`

2. **JSON Data File**: Raw scraped data (for debugging)
   - Example: `2025_April_data.json`

## Troubleshooting

### Import Errors

If you get import errors, make sure all dependencies are installed:

```bash
pip install --upgrade reportlab
```

### Network Errors

If scraping fails, check your internet connection and verify the conference URL is correct.

### PDF Generation Issues

If PDF generation fails, check that you have write permissions in the output directory.

## Customization

### Modify PDF Styling

Edit `pdf_generator.py` and modify the `_setup_custom_styles()` method to change:
- Font sizes
- Colors
- Spacing
- Alignment

### Change Scraping Behavior

Edit `conference_scraper.py` to:
- Filter specific types of talks
- Extract additional metadata
- Modify text extraction logic

## Notes

- The script respects the Church's website structure and uses their public API
- Scraping may take several minutes depending on the number of talks
- Generated PDFs match the format of the example in `example/2025_April.pdf`

## License

This tool is provided as-is for personal use. Please respect the Church's copyright and terms of service when using scraped content.

## Support

For issues or questions, please check:
1. Python version (3.7+)
2. All dependencies installed
3. Valid conference URL format
4. Internet connection

## Version History

- **v1.0** (2025-10-05): Initial release
  - Web scraping functionality
  - PDF generation with formatting
  - Support for different conference years/sessions

