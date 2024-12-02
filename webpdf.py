#!/usr/bin/env python3

import sys
import os
import argparse
import platform
import shutil
import subprocess
import requests
import pdfkit
from tqdm.auto import tqdm


class DependencyChecker:
    AVAILABLE = "\033[92m✓\033[0m"
    MISSING = "\033[91m✗\033[0m"
    WARN = "\033[93m!\033[0m"

    @classmethod
    def check_dependencies(cls):
        deps = {
            "wkhtmltopdf": cls._check_wkhtmltopdf(),
            "python3": cls._check_python(),
            "pip": cls._check_pip(),
            "tqdm": cls._check_tqdm(),
            "pdfkit": cls._check_pdfkit()
        }

        print("\nDependency Check:")
        for dep, status in deps.items():
            print(f"{dep}: {status}")

        if any(status == cls.MISSING for status in deps.values()):
            print("\nMissing Dependencies:")
            cls._print_installation_guide(deps)
            sys.exit(1)

    @classmethod
    def _check_wkhtmltopdf(cls):
        return cls.AVAILABLE if shutil.which("wkhtmltopdf") else cls.MISSING

    @classmethod
    def _check_python(cls):
        try:
            subprocess.run(["python3", "--version"],
                           capture_output=True, text=True)
            return cls.AVAILABLE
        except FileNotFoundError:
            return cls.MISSING

    @classmethod
    def _check_pip(cls):
        try:
            subprocess.run(["pip3", "--version"],
                           capture_output=True, text=True)
            return cls.AVAILABLE
        except FileNotFoundError:
            return cls.MISSING

    @classmethod
    def _check_tqdm(cls):
        try:
            import tqdm
            return cls.AVAILABLE
        except ImportError:
            return cls.MISSING

    @classmethod
    def _check_pdfkit(cls):
        try:
            import pdfkit
            return cls.AVAILABLE
        except ImportError:
            return cls.MISSING

    @classmethod
    def _print_installation_guide(cls, deps):
        system = platform.system().lower()

        if deps["wkhtmltopdf"] == cls.MISSING:
            print(f"\n{cls.WARN} Install wkhtmltopdf:")
            if system == "windows":
                print("  Download from: https://wkhtmltopdf.org/downloads.html")
            elif system == "darwin":
                print("  Run: brew install wkhtmltopdf")
            else:
                print("  Run: sudo apt-get install wkhtmltopdf")

        if any(deps[lib] == cls.MISSING for lib in ["pip", "tqdm", "pdfkit"]):
            print(f"\n{cls.WARN} Python Dependencies:")
            print("  Run: pip3 install tqdm pdfkit")


class WebPDFConverter:
    SUCCESS = "\033[92m✔\033[0m"
    FAILURE = "\033[91m✘\033[0m"

    @staticmethod
    def check_url_connection(url):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code >= 400:
                raise Exception(f"Received HTTP {
                                response.status_code} from the server.")
            print(f"Connection Test: URL is reachable {
                  WebPDFConverter.SUCCESS}")
        except Exception as e:
            print(f"Connection Test: Warning - {e} {WebPDFConverter.FAILURE}")
            print("Proceeding with the conversion. Ensure the URL is valid.")

    @staticmethod
    def detect_javascript(url):
        try:
            response = requests.get(url, timeout=5)
            if "<script" in response.text:
                return True
        except Exception as e:
            print(
                f"JavaScript Detection: Warning - {e} {WebPDFConverter.FAILURE}")
        return False

    @classmethod
    def convert_to_pdf(cls, url, output_pdf):
        try:
            print("Converting to PDF...", end=' ', flush=True)
            options = {
                'enable-javascript': None,
                'javascript-delay': 10000,
                'no-stop-slow-scripts': None
            }

            if cls.detect_javascript(url):
                options['javascript-delay'] = 15000
                print(f"\nJavaScript detected. Increasing delay to {
                      options['javascript-delay']} ms.")

            pdfkit.from_url(url, output_pdf, options=options)
            cls._print_status(f"Success! PDF saved to: {
                              output_pdf}", cls.SUCCESS)

        except Exception as e:
            print(f"\bError {cls.FAILURE}")
            cls._print_status(f"Error: {e}", cls.FAILURE)
            sys.exit(1)

    @staticmethod
    def _print_status(message, status):
        print(f"{message} {status}")

    @staticmethod
    def generate_output_path(input_path, output_filename=None):
        def validate_filename(filename):
            safe_filename = ''.join(
                c for c in filename if c.isalnum() or c in ('-', '_', '.'))
            if not safe_filename or set(safe_filename) <= {'.'}:
                raise ValueError("Invalid filename")
            return safe_filename

        def create_directory(path):
            try:
                os.makedirs(path, exist_ok=True)
                print(f"Directory created: {path}")
            except PermissionError:
                print(f"Error: No permission to create directory {path}")
                sys.exit(1)
            except Exception as e:
                print(f"Error creating directory: {e}")
                sys.exit(1)

        save_dir = os.path.expanduser("~/Downloads/WebPDFs")
        if not os.path.exists(save_dir):
            create_directory(save_dir)

        if output_filename:
            output_filename = input_path.split("//")[-1].split("/")[0] if input_path.startswith(
                ("http://", "https://")) else os.path.splitext(os.path.basename(input_path))[0]
            output_filename += '.pdf'
            output_path = os.path.join(save_dir, output_filename)
        else:
            output_filename = input_path.split("//")[-1].split("/")[0] if input_path.startswith(
                ("http://", "https://")) else os.path.splitext(os.path.basename(input_path))[0]
            output_filename += '.pdf'
            output_path = os.path.join(save_dir, output_filename)

        try:
            validate_filename(os.path.basename(output_path))
        except ValueError:
            print("Error: Invalid filename")
            sys.exit(1)

        base, ext = os.path.splitext(output_path)
        counter = 1
        while os.path.exists(output_path):
            output_path = f"{base}({counter}){ext}"
            counter += 1

        print(f"Generated output path: {output_path}")
        return output_path


def main():
    DependencyChecker.check_dependencies()
    parser = argparse.ArgumentParser(description="Save a webpage as a PDF.")
    parser.add_argument("input", help="URL or path to a local HTML file")
    parser.add_argument(
        "-o", "--output", help="Optional output filename or directory", default=None)
    args = parser.parse_args()
    WebPDFConverter.check_url_connection(args.input)
    output_path = WebPDFConverter.generate_output_path(args.input, args.output)
    WebPDFConverter.convert_to_pdf(args.input, output_path)
    print("\nHappy reading! \U0001F604")


if __name__ == "__main__":
    main()
