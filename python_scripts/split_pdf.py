#!/usr/bin/env python

import subprocess
import argparse
import math
import os

def get_pdf_page_count(pdf_path):
    """
    Gets the number of pages in a PDF file using pdfinfo.
    """
    try:
        # Run pdfinfo and capture its output
        process = subprocess.run(
            ['pdfinfo', pdf_path],
            capture_output=True,
            text=True,
            check=True # Raise an exception for non-zero exit codes
        )
        output = process.stdout
        
        # Look for the "Pages:" line in the output
        for line in output.splitlines():
            if "Pages:" in line:
                try:
                    return int(line.split(":")[1].strip())
                except (ValueError, IndexError):
                    raise ValueError(f"Could not parse page count from pdfinfo output line: {line}")
        raise ValueError("Could not find 'Pages:' in pdfinfo output. Is the PDF valid?")
    except FileNotFoundError:
        print("Error: 'pdfinfo' command not found. Please ensure 'poppler-utils' is installed.")
        print("On Arch Linux, you can install it with: sudo pacman -S poppler-utils")
        exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running pdfinfo for '{pdf_path}': {e.stderr.strip()}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while getting page count: {e}")
        exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Split a PDF into multiple parts using qpdf.",
        epilog="""
Example usage:
  python split_pdf.py my_document.pdf                  # Asks for number of parts
  python split_pdf.py my_document.pdf -n 3             # Splits into 3 parts
  python split_pdf.py --help                           # Shows this help message
"""
    )
    parser.add_argument(
        "pdf_path",
        help="Path to the PDF file to split."
    )
    parser.add_argument(
        "-n", "--num-parts",
        type=int,
        help="Number of parts to split the PDF into. If not provided, you'll be asked interactively."
    )

    args = parser.parse_args()

    pdf_file = args.pdf_path
    num_parts = args.num_parts

    # --- Input Validation ---
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file '{pdf_file}' not found.")
        exit(1)
    if not os.path.isfile(pdf_file):
        print(f"Error: '{pdf_file}' is not a file.")
        exit(1)

    print(f"🔍 Getting page count for '{pdf_file}'...")
    total_pages = get_pdf_page_count(pdf_file)
    print(f"✅ Total pages: {total_pages}")

    # --- Get Number of Parts from User or Argument ---
    if num_parts is None:
        while True:
            try:
                user_input = input(f"Enter the number of parts to split the PDF into (e.g., 3, max {total_pages}): ")
                num_parts = int(user_input)
                if num_parts < 1:
                    print("Please enter a number greater than or equal to 1.")
                elif num_parts > total_pages:
                    print(f"You asked for {num_parts} parts, but the PDF only has {total_pages} pages. Adjusting to {total_pages} parts.")
                    num_parts = total_pages
                    break
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a whole number.")
    else: # num_parts was provided via argument
        if num_parts < 1:
            print("Error: Number of parts must be greater than or equal to 1.")
            exit(1)
        if num_parts > total_pages:
            print(f"⚠️ Warning: You specified {num_parts} parts, but the PDF only has {total_pages} pages. Adjusting to {total_pages} parts.")
            num_parts = total_pages

    print(f"\n✂️ Splitting '{pdf_file}' into {num_parts} parts...")

    base_name = os.path.splitext(os.path.basename(pdf_file))[0]  # just the file name without path
    extension = os.path.splitext(pdf_file)[1]
    
    # Create output directory based on PDF name
    output_dir = f"{base_name}_parts"
    os.makedirs(output_dir, exist_ok=True)  # Creates the dir if it doesn't exist
    
    # Calculate pages per part, ensuring even distribution
    pages_per_part = math.ceil(total_pages / num_parts)
    current_page = 1

    print("\n🚀 Executing `qpdf` commands...")
    print("--------------------------------------------------------------------------------")
    
    successful_splits = 0
    for i in range(num_parts):
        start_page = current_page
        end_page = min(current_page + pages_per_part - 1, total_pages)
        
        # Ensure the last part covers all remaining pages
        if i == num_parts - 1:
            end_page = total_pages

        output_filename = os.path.join(output_dir, f"{base_name}_part{i+1}{extension}")
        
        # Construct the command as a list for subprocess.run for better security and handling of spaces
        qpdf_command = [
            'qpdf',
            pdf_file,
            '--pages',
            '.', # Important: refers to pages of the input PDF
            f'{start_page}-{end_page}',
            '--',
            output_filename
        ]

        print(f"  [{i+1}/{num_parts}] Creating '{output_filename}' (pages {start_page}-{end_page})...", end=" ")
        try:
            # Run the qpdf command
            subprocess.run(qpdf_command, check=True, capture_output=True, text=True)
            print(f"  ✅ Successfully created '{output_filename}'")
            successful_splits += 1
        except FileNotFoundError:
            print()
            print("\nError: 'qpdf' command not found. Please ensure 'qpdf' is installed.")
            print("On Arch Linux, you can install it with: sudo pacman -S qpdf")
            exit(1)
        except subprocess.CalledProcessError as e:
            print()
            print(f"  ❌ Failed to create '{output_filename}'.")
            print(f"     qpdf error: {e.stderr.strip()}")
            print(f"     Command tried: {' '.join(qpdf_command)}")
            # Don't exit immediately, try to process other parts
        except Exception as e:
            print()
            print(f"  ❌ An unexpected error occurred while creating '{output_filename}': {e}")
        
        current_page = end_page + 1
    
    print("--------------------------------------------------------------------------------")
    if successful_splits == num_parts:
        print(f"\n🎉 All {num_parts} parts successfully created in the current directory!")
    elif successful_splits > 0:
        print(f"\n⚠️ Finished. {successful_splits} out of {num_parts} parts were successfully created.")
    else:
        print("\n❌ No PDF parts were successfully created. Please check the error messages above.")

if __name__ == "__main__":
    main()

