import csv
import os
import requests
import urllib.parse
import re
from pathlib import Path


def clean_url(url):
    pattern = re.compile(r'^(https?:)https?://', re.IGNORECASE)
    cleaned_url = pattern.sub(r'\1//', url)
    return cleaned_url

def download_images_and_update_csv(input_csv_path, output_csv_path, images_folder='images'):
    os.makedirs(images_folder, exist_ok=True)

    with open(input_csv_path, mode='r', encoding='utf-8', newline='') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        updated_rows = []

        for row in reader:
            image_url = row.get('imageUrl', '').strip()
            image_url = clean_url(image_url)

            if image_url:
                try:
                    response = requests.get(image_url, timeout=10)
                    response.raise_for_status()

                    parsed_url = urllib.parse.urlparse(image_url)
                    filename = os.path.basename(parsed_url.path)
                    if not filename:
                        filename = f"image_{row.get('Nid','unknown')}.jpg"

                    local_image_path = os.path.join(images_folder, filename)

                    with open(local_image_path, 'wb') as f:
                        f.write(response.content)

                    absolute_image_path = os.path.abspath(local_image_path)

                    row['imageUrl'] = absolute_image_path

                except requests.exceptions.RequestException as e:
                    print(f"Failed to download {image_url}: {e}")
                    row['imageUrl'] = ''
            else:
                row['imageUrl'] = ''

            updated_rows.append(row)

    with open(output_csv_path, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

import csv
import os
import urllib.parse
from pathlib import Path

def extract_filename_from_url(url):
    """
    Extracts the filename from a given URL.

    :param url: The URL string.
    :return: The filename extracted from the URL, or None if extraction fails.
    """
    if not url:
        return None
    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename if filename else None

def replace_image_urls_with_local_paths(input_csv_path, output_csv_path, images_folder_path):
    """
    Reads the input CSV, replaces the 'imageUrl' field with the absolute path
    of the corresponding image from the local images folder, and writes the
    updated data to a new CSV file.

    :param input_csv_path: Path to the input CSV file.
    :param output_csv_path: Path where the updated CSV file will be written.
    :param images_folder_path: Path to the folder containing local images.
    """
    images_folder = Path(images_folder_path)

    if not images_folder.exists() or not images_folder.is_dir():
        raise FileNotFoundError(f"The images folder '{images_folder}' does not exist or is not a directory.")

    with open(input_csv_path, mode='r', encoding='utf-8', newline='') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        if 'imageUrl' not in fieldnames:
            raise ValueError("The input CSV does not contain an 'imageUrl' column.")

        updated_rows = []
        missing_images = []

        for row in reader:
            original_url = row.get('imageUrl', '').strip()
            filename = extract_filename_from_url(original_url)

            if filename:
                local_image_path = images_folder / filename
                if local_image_path.exists() and local_image_path.is_file():
                    absolute_path = str(local_image_path.resolve())
                    row['imageUrl'] = absolute_path
                else:
                    print(f"Warning: Image file '{filename}' not found in '{images_folder}'.")
                    missing_images.append(filename)
                    row['imageUrl'] = ''  # Optionally, retain the original URL: row['imageUrl'] = original_url
            else:
                print(f"Warning: Could not extract filename from URL: '{original_url}'.")
                row['imageUrl'] = ''  # Optionally, retain the original URL: row['imageUrl'] = original_url

            updated_rows.append(row)

    # Write the updated rows to the output CSV
    with open(output_csv_path, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"\nCSV update complete. Updated file saved as '{output_csv_path}'.")

    if missing_images:
        print(f"\nTotal missing images: {len(missing_images)}")
        # Optionally, write missing images to a log file
        with open('missing_images.log', mode='w', encoding='utf-8') as log_file:
            for img in missing_images:
                log_file.write(f"{img}\n")
        print("A list of missing images has been saved to 'missing_images.log'.")

if __name__ == '__main__':
    # Define paths
    input_csv = './output.csv'           # Path to your existing CSV
    output_csv = './updated_output.csv'  # Desired path for the updated CSV
    images_folder = './images'           # Path to your images folder

    # Update the CSV
    try:
        replace_image_urls_with_local_paths(input_csv, output_csv, images_folder)
    except Exception as e:
        print(f"An error occurred: {e}")
