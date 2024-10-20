WebPDF

Sometimes, you come across a webpage that is so good you have to save it for later :) That's exactly why I created this script.

WebPDF is a Python script that provides a simple interface to convert web pages or HTML files into PDF documents using the wkhtmltopdf library. This script allows users to easily generate PDFs from URLs or local HTML files with various configuration options.

## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Add to PATH](#add-to-path)
- [Usage](#usage)
- [Examples](#examples)
- [Notes](#notes)
- [Progress Updates](#progress-updates)

## Features

- Convert web pages to PDF using URLs.
- Convert local HTML files to PDF.
- Automatically checks for required dependencies (pdfkit and wkhtmltopdf).
- Uses pipx for dependency installation if available.

## Dependencies

This script requires the following:

- **pdfkit**: A Python wrapper for wkhtmltopdf that simplifies the process of generating PDFs.
- **wkhtmltopdf**: A command-line tool to render HTML into PDF and other formats.

You can install pdfkit via pipx (preferred) or pip:

```bash
# Install via pipx
pipx install pdfkit

# Or install via pip
pip install pdfkit
```

Additionally, you need to have wkhtmltopdf installed on your system. You can install it using the following commands based on your operating system:

### For Ubuntu/Debian

```bash
sudo apt-get install wkhtmltopdf
```

### For macOS

```bash
brew install wkhtmltopdf
```

### For Windows

Download the installer from the wkhtmltopdf website and follow the installation instructions.

## Installation

### Step 1: Clone the Repository

```bash
git clone <https://github.com/BarriosXJavier/WebPDF.git>
cd webpdf
```

### Step 2: Set Executable Permissions (Linux/macOS)

On Linux or macOS, you'll need to make the script executable by running:

```bash
chmod +x webpdf.py
```

### Step 3: Install Dependencies

Ensure you have installed pdfkit (using pipx or pip) and wkhtmltopdf as described in the Dependencies section.

## Add to PATH

To make the webpdf.py script available globally so that you can run it from any directory, you can add it to your system's PATH.

### Linux/macOS

Move the script to a directory that is already in your PATH or create a symbolic link:

```bash
sudo mv webpdf.py /usr/local/bin/webpdf
```

Alternatively, create a symlink:

```bash
ln -s $(pwd)/webpdf.py /usr/local/bin/webpdf
```

Ensure /usr/local/bin is in your PATH. You can check by running:

```bash
echo $PATH
```

If it's not in your PATH, you can add it by adding the following line to your `~/.bashrc` (for Bash users) or `~/.zshrc` (for Zsh users):

```bash
export PATH="/usr/local/bin:$PATH"
```

After adding, run:

```bash
source ~/.bashrc   # For Bash users
# or
source ~/.zshrc    # For Zsh users
```

### Windows

Copy the script to a directory included in the system PATH, or modify the PATH to include the script's directory. Here’s how to add it to PATH:

1. Go to Control Panel > System and Security > System > Advanced System Settings.
2. Click on Environment Variables.
3. In the System Variables section, find the Path variable, select it, and click Edit.
4. Add the full path to the folder containing webpdf.py (for example, C:\path\to\webpdf\).

Once added, you should be able to run the script by typing `webpdf.py` in any terminal or command prompt window.

## Usage

To use the script, run the following command in your terminal:

```bash
webpdf [options] <url_or_html_file>
```

This assumes you've added the script to your PATH (as described in the section above).

If not, you can still run it by calling:

```bash
python3 /path/to/webpdf.py [options] <url_or_html_file>
```

## Examples

### Convert a URL to PDF

```bash
webpdf <https://www.example.com>
```

### Convert a Local HTML File to PDF

```bash
webpdf local_file.html
```

## Notes

- The script will automatically check if pdfkit is installed and attempt to install it via pipx if not present. If pipx is not available, it will abort and notify you.
- The script will check if wkhtmltopdf is installed and provide instructions to install it if missing.
