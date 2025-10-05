# Quick Reference Card

## Setup (First Time Only)

```bash
./setup.sh
```

## Every Time You Use It

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Run the script (ALWAYS USE QUOTES!)
python generate_conference_pdf.py "URL_HERE"

# 3. Deactivate when done
deactivate
```

## Common Commands

### Generate April 2025 Conference
```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"
```

### Generate October 2024 Conference
```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2024/10?lang=eng"
```

### Custom Output Name
```bash
python generate_conference_pdf.py "URL_HERE" output_name.pdf
```

## ⚠️ Common Mistakes

### ❌ WRONG - No quotes
```bash
python generate_conference_pdf.py https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng
# Error: zsh: no matches found
```

### ✅ CORRECT - With quotes
```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"
```

### ❌ WRONG - Forgot to activate venv
```bash
python generate_conference_pdf.py "URL"
# Error: command not found or module not found
```

### ✅ CORRECT - Activate first
```bash
source venv/bin/activate
python generate_conference_pdf.py "URL"
```

## URL Format

```
https://www.churchofjesuschrist.org/study/general-conference/YYYY/MM?lang=eng
                                                              ^^^^  ^^
                                                              Year  Month
```

- **April conferences:** Use `04`
- **October conferences:** Use `10`

## Output Files

Running the script creates:
- `YYYY_Month.pdf` - The formatted PDF
- `YYYY_Month_data.json` - Raw data backup

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `zsh: no matches found` | Add quotes around URL |
| `command not found` | Run `source venv/bin/activate` |
| `No module named 'reportlab'` | Run `./setup.sh` again |
| `HTTP Error 404` | Check URL format is correct |
| Script is slow | Normal! Takes 1-2 minutes |

## Need More Help?

- Full docs: `README.md`
- Getting started: `GETTING_STARTED.md`
- Usage guide: `USAGE_GUIDE.md`

## One-Liner (Copy & Paste)

```bash
source venv/bin/activate && python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng" && deactivate
```

This activates venv, runs the script, and deactivates when done.

