# Quick Usage Guide

## First Time Setup

1. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

## Generating a Conference PDF

### Basic Usage

```bash
python generate_conference_pdf.py <conference_url>
```

### Examples

**April 2025 General Conference:**
```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"
```

**October 2024 General Conference:**
```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2024/10?lang=eng"
```

**Custom Output Filename:**
```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng" MyConference.pdf
```

**Important:** Always wrap the URL in quotes to prevent shell expansion issues with the `?` character.

## What Gets Generated

The script creates two files:

1. **PDF File** - The formatted conference document
   - Example: `2025_April.pdf`
   - Contains cover page, table of contents, and all talks

2. **JSON Data File** - Raw scraped data (for debugging)
   - Example: `2025_April_data.json`
   - Contains all talk content in JSON format

## Process Overview

The script performs these steps:

1. **Scrapes Conference Data**
   - Fetches the conference page
   - Extracts all talk links
   - Downloads each talk's content
   - Parses HTML to clean text

2. **Generates PDF**
   - Creates cover page
   - Builds table of contents
   - Formats each talk with speaker and title
   - Applies professional styling

## Typical Runtime

- **Small conference** (10-15 talks): ~30 seconds
- **Full conference** (30-40 talks): ~1-2 minutes

The script shows progress as it works.

## Tips

- **Always activate the virtual environment first:**
  ```bash
  source venv/bin/activate
  ```

- **Check your internet connection** - The script needs to download content from churchofjesuschrist.org

- **Be patient** - Scraping 30+ talks takes time

- **Keep the JSON file** - It's useful if you want to regenerate the PDF with different formatting

## Troubleshooting

### "no matches found" error
If you see: `zsh: no matches found: https://...`

**Solution:** Wrap the URL in quotes:
```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"
```

The `?` character in the URL needs to be quoted to prevent shell expansion.

### "Command not found" error
Make sure you've activated the virtual environment:
```bash
source venv/bin/activate
```

### "Module not found" error
Install dependencies:
```bash
pip install -r requirements.txt
```

### Network errors
- Check your internet connection
- Verify the conference URL is correct
- Try again in a few minutes

### PDF looks wrong
The PDF formatting is designed to be clean and readable. If you want to customize it, edit `pdf_generator.py`.

## Advanced Usage

### Scrape Only (No PDF)

To just scrape data without generating a PDF:

```bash
python conference_scraper.py "<conference_url>"
```

This creates a JSON file with all the data.

### Generate PDF from Existing JSON

If you already have scraped data:

```bash
python pdf_generator.py <json_file> <output_pdf>
```

Example:
```bash
python pdf_generator.py 2025_April_data.json MyCustom.pdf
```

## Deactivating the Virtual Environment

When you're done:

```bash
deactivate
```

## Getting Help

If you encounter issues:

1. Check this guide
2. Read the README.md
3. Verify Python 3.7+ is installed: `python3 --version`
4. Make sure dependencies are installed: `pip list`
5. Check the conference URL is valid

## Example Output

The generated PDF includes:

- **Cover Page**: Conference title and date
- **Table of Contents**: List of all talks with speakers
- **Individual Talks**: Each talk on separate pages with:
  - Talk title (centered, bold)
  - Speaker name (centered, italic)
  - Full talk content (justified text)

The formatting matches professional document standards and is optimized for readability.

