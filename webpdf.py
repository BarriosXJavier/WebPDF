#!/usr/bin/env python3

import sys
import os
import argparse
import subprocess
import platform


def check_dependencies():
    try:
        import pdfkit
    except ImportError:
        print("pdfkit is not installed. Installing it now...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pdfkit"])
        import pdfkit


def get_wkhtmltopdf_path():
    system = platform.system().lower()
    if system == "windows":
        return r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    elif system == "darwin":  # macOS
        return "/usr/local/bin/wkhtmltopdf"
    else:  # Linux and others
        return "/usr/bin/wkhtmltopdf"


def install_wkhtmltopdf():
    system = platform.system().lower()
    print(f"wkhtmltopdf is not installed. Please install it manually:")
    if system == "windows":
        print("Download and install from: https://wkhtmltopdf.org/downloads.html")
    elif system == "darwin":  # macOS
        print("Run: brew install wkhtmltopdf")
    else:  # Linux and others : )
        print("Run: sudo apt-get install wkhtmltopdf")
    print("After installation, rerun this script.")
    sys.exit(1)


def save_to_pdf(url, output_pdf, wkhtmltopdf_path):
    try:
        import pdfkit
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        options = {'quiet': ''}

        if url.startswith(("http://", "https://")):
            print(f"Converting webpage: {url} to PDF...")
            pdfkit.from_url(url, output_pdf,
                            configuration=config, options=options)
        elif os.path.isfile(url):
            print(f"Converting local file: {url} to PDF...")
            pdfkit.from_file(
                url, output_pdf, configuration=config, options=options)
        else:
            raise ValueError("The URL is not valid or the file was not found.")
        print(f"Success! PDF saved to: {output_pdf}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Save a webpage or HTML file as a PDF.")
    parser.add_argument("input", help="URL or path to the local HTML file")
    parser.add_argument(
        "--output", help="Output directory (default: ~/Downloads/WebPDFs)", default=None)
    args = parser.parse_args()

    check_dependencies()

    wkhtmltopdf_path = get_wkhtmltopdf_path()
    if not os.path.exists(wkhtmltopdf_path):
        install_wkhtmltopdf()

    input_path = args.input
    output_filename = input(
        "Enter the desired output file name (without .pdf extension): ")
    if output_filename.endswith('.pdf'):
        output_filename = output_filename[:-4]

    if args.output:
        save_dir = os.path.expanduser(args.output)
    else:
        save_dir = os.path.expanduser("~/Downloads/WebPDFs")
    os.makedirs(save_dir, exist_ok=True)

    output_path = os.path.join(save_dir, f"{output_filename}.pdf")

    save_to_pdf(input_path, output_path, wkhtmltopdf_path)


if __name__ == "__main__":
    main()
