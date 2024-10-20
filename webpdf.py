#!/usr/bin/env python3

import sys
import os
import argparse
import subprocess
import platform
import shutil

SUCCESS = "\033[92m✔\033[0m"  # Green checkmark
FAILURE = "\033[91m✘\033[0m"  # Red cross
INFO = "\033[94mℹ\033[0m"     # Blue info symbol


def print_status(message, status):
    print(f"{message} {status}")


def check_dependencies():
    print(f"{INFO} Checking dependencies...")
    try:
        import pdfkit
        print_status("pdfkit is installed", SUCCESS)
    except ImportError:
        print_status("pdfkit is not installed", FAILURE)
        if shutil.which("pipx"):
            print(f"{INFO} Attempting to install pdfkit via pipx...")
            subprocess.check_call(["pipx", "install", "pdfkit"])
            print_status("pdfkit installation complete", SUCCESS)
            import pdfkit
        else:
            print_status("pipx is not installed", FAILURE)
            print(f"{INFO} pipx is required to install dependencies. Aborting.")
            sys.exit(1)


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
    print_status("wkhtmltopdf is not installed", FAILURE)
    print(f"{INFO} Please install wkhtmltopdf manually:")
    if system == "windows":
        print("Download and install from: https://wkhtmltopdf.org/downloads.html")
    elif system == "darwin":  # macOS
        print("Run: brew install wkhtmltopdf")
    else:  # Linux and others
        print("Run: sudo apt-get install wkhtmltopdf")
    print(f"{INFO} After installation, rerun this script.")
    sys.exit(1)


def save_to_pdf(url, output_pdf, wkhtmltopdf_path):
    try:
        import pdfkit
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        options = {'quiet': ''}

        if url.startswith(("http://", "https://")):
            print(f"{INFO} Converting webpage: {url} to PDF...")
            pdfkit.from_url(url, output_pdf,
                            configuration=config, options=options)
        elif os.path.isfile(url):
            print(f"{INFO} Converting local file: {url} to PDF...")
            pdfkit.from_file(
                url, output_pdf, configuration=config, options=options)
        else:
            raise ValueError("The URL is not valid or the file was not found.")
        print_status(f"Success! PDF saved to: {output_pdf}", SUCCESS)
    except Exception as e:
        print_status(f"Error: {e}", FAILURE)
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
