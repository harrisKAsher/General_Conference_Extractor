# Getting Started with General Conference PDF Generator

## 🚀 Quick Start (3 Steps)

### Step 1: Setup
```bash
./setup.sh
```

### Step 2: Activate
```bash
source venv/bin/activate
```

### Step 3: Run
```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"
```

**Note:** The quotes around the URL are important!

That's it! You'll get a PDF file named `2025_April.pdf`.

---

## 📋 What You Need

- **Python 3.7+** (check with `python3 --version`)
- **Internet connection** (to download conference talks)
- **5 minutes** for setup and first run

---

## 📖 Detailed Instructions

### First Time Setup

1. **Open Terminal** and navigate to the project directory:
   ```bash
   cd /path/to/Scripture_Extractor
   ```

2. **Run the setup script:**
   ```bash
   ./setup.sh
   ```
   
   This will:
   - Create a virtual environment
   - Install required packages (reportlab)
   - Verify everything is working

3. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```
   
   You'll see `(venv)` appear in your terminal prompt.

### Generating Your First PDF

**Basic command:**
```bash
python generate_conference_pdf.py <conference_url>
```

**Example - April 2025 Conference:**
```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"
```

**What happens:**
1. Script connects to churchofjesuschrist.org
2. Downloads all talks from the conference
3. Generates a formatted PDF
4. Saves two files:
   - `2025_April.pdf` (the formatted document)
   - `2025_April_data.json` (raw data backup)

**Time:** About 1-2 minutes for a full conference

### Using a Custom Filename

```bash
python generate_conference_pdf.py <url> <filename>
```

**Example:**
```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng" MyConference.pdf
```

---

## 🎯 Common Use Cases

### Generate April 2025 Conference
```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"
```

### Generate October 2024 Conference
```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2024/10?lang=eng"
```

### Generate April 2024 Conference
```bash
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2024/04?lang=eng"
```

---

## 📁 What Gets Created

After running the script, you'll have:

```
Scripture_Extractor/
├── 2025_April.pdf           ← Your formatted PDF
└── 2025_April_data.json     ← Raw data (for debugging)
```

### The PDF Contains:
1. **Cover Page** - Conference title and date
2. **Table of Contents** - All talks with speakers
3. **Individual Talks** - Each talk formatted with:
   - Speaker name
   - Talk title
   - Full content

---

## 🔧 Troubleshooting

### Problem: "command not found: ./setup.sh"
**Solution:** Make the script executable:
```bash
chmod +x setup.sh
./setup.sh
```

### Problem: "python: command not found"
**Solution:** Use `python3` instead:
```bash
python3 generate_conference_pdf.py <url>
```

### Problem: "No module named 'reportlab'"
**Solution:** Activate virtual environment and install:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: "HTTP Error 404"
**Solution:** Check the conference URL is correct. Format should be:
```
https://www.churchofjesuschrist.org/study/general-conference/YYYY/MM?lang=eng
```
Where YYYY is year and MM is month (04 or 10).

### Problem: Script is slow
**Solution:** This is normal! Downloading 30+ talks takes 1-2 minutes. You'll see progress messages.

---

## 💡 Tips & Tricks

### Tip 1: Always Activate Virtual Environment
Before running the script, always activate:
```bash
source venv/bin/activate
```

You'll see `(venv)` in your prompt when it's active.

### Tip 2: Keep the JSON File
The `*_data.json` file is useful if you want to:
- Regenerate the PDF with different formatting
- Debug issues
- Extract specific talks

### Tip 3: Batch Processing
Generate multiple conferences:
```bash
source venv/bin/activate
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2024/10?lang=eng"
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2024/04?lang=eng"
```

### Tip 4: Deactivate When Done
When finished:
```bash
deactivate
```

---

## 📚 More Information

- **Full Documentation:** See `README.md`
- **Quick Reference:** See `USAGE_GUIDE.md`
- **Technical Details:** See `PROJECT_STRUCTURE.md`

---

## ✅ Verification

To verify everything is working:

1. **Check Python version:**
   ```bash
   python3 --version
   ```
   Should show 3.7 or higher.

2. **Check virtual environment:**
   ```bash
   source venv/bin/activate
   python --version
   ```
   Should show Python 3.x.

3. **Check dependencies:**
   ```bash
   pip list | grep reportlab
   ```
   Should show reportlab is installed.

4. **Run test:**
   ```bash
   python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng" test.pdf
   ```
   Should create `test.pdf` successfully.

---

## 🎉 Success!

If you see this message, you're done:

```
================================================================================
COMPLETE!
================================================================================

Conference: April 2025 general conference
Total talks: 34

Output files:
  - PDF: 2025_April.pdf
  - JSON data: 2025_April_data.json

================================================================================
```

Open the PDF and enjoy reading the conference talks!

---

## 🆘 Need Help?

1. Read the error message carefully
2. Check the Troubleshooting section above
3. Verify your internet connection
4. Make sure the conference URL is correct
5. Try running `./setup.sh` again

---

## 📝 Example Session

Here's what a complete session looks like:

```bash
# Navigate to project
cd /Users/asherharris/PycharmProjects/Scripture_Extractor

# First time setup (only needed once)
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Generate PDF
python generate_conference_pdf.py "https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng"

# Wait 1-2 minutes...
# PDF is created!

# Deactivate when done
deactivate
```

---

**Happy Conference Reading! 📖**

