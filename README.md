# WebPDF

Sometimes, you come across a webpage that is so good you have to save it for later :) That's exactly why I created this script.

WebPDF is a Python script  that provides a simple interface to convert web pages or HTML files into PDF documents using the `wkhtmltopdf` library. This script allows users to easily generate PDFs from URLs or local HTML files with various configuration options.

## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)

## Features

- Convert web pages to PDF using URLs.
- Convert local HTML files to PDF.

## Dependencies

This script requires the following Python packages:

- `wkhtmltopdf`: A simple Python wrapper for the `wkhtmltopdf` utility.
- `pdfkit`: A Python wrapper for `wkhtmltopdf` that simplifies the process of generating PDFs.

You can install these dependencies using pip:

```bash
pip install pdfkit
```

Additionally, you need to have `wkhtmltopdf` installed on your system. You can install it using the following commands based on your operating system:

### For Ubuntu/Debian

```bash
sudo apt-get install wkhtmltopdf
```

### For macOS

```bash
brew install wkhtmltopdf
```

### For Windows

Download the installer from the [wkhtmltopdf website](https://wkhtmltopdf.org/downloads.html) and follow the installation instructions.

## Installation

1. Clone the repository or download the script.
2. Ensure that all dependencies are installed as mentioned above.
3. Make sure `wkhtmltopdf` is accessible in your system's PATH.

## Usage

To use the script, run the following command in your terminal:

```bash
python webpdf.py [options] <url_or_html_file> <output_pdf_file>
```

## Examples

### Convert a URL to PDF

```bash
python3 webpdf.py https://www.example.com output.pdf
```

### Convert a Local HTML File to PDF

```bash
python webpdf.py local_file.html output.pdf
```
