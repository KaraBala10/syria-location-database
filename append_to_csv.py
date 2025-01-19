import csv
import os

from deep_translator import GoogleTranslator


def translate(text):
    """Translate Arabic text to English using GoogleTranslator."""
    try:
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def parse_directory_and_generate_csv(input_dir, output_file):
    """
    Parses the directory to extract data from text files and saves only new records to a CSV file.
    Also generates a report of the number of towns from each file.
    """

    data = []  # New data to write
    report = {}  # Report of the number of towns per file
    existing_rows = set()  # Set to store existing rows for quick lookup

    # Step 1: Read existing CSV data if the file already exists
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Skip the header row
            for row in reader:
                existing_rows.add(tuple(row))  # Store each row as a tuple in the set

    # Step 2: Process text files and extract data
    for governorate_folder in os.listdir(input_dir):
        governorate_path = os.path.join(input_dir, governorate_folder)
        if not os.path.isdir(governorate_path):
            continue  # Skip non-directories

        for city_file in os.listdir(governorate_path):
            city_path = os.path.join(governorate_path, city_file)
            if not city_file.endswith(".txt"):
                continue  # Skip non-text files

            # Read the file contents
            with open(city_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Extract governorate and city
            governorate = governorate_folder
            city = os.path.splitext(city_file)[0]
            subdistrict = ""
            town_count = 0  # Counter for towns in the current file

            for line in lines:
                stripped = line.strip()

                # Detect subdistrict
                if stripped.startswith("بلدات وقرى ناحية"):
                    subdistrict = stripped.replace("بلدات وقرى ناحية", "").strip()

                # Detect town and check if it's a duplicate
                elif stripped and not stripped.startswith("بلدات وقرى ناحية"):
                    row = (governorate, city, subdistrict, stripped)
                    if row not in existing_rows:  # Only add new rows
                        data.append(row)
                        existing_rows.add(row)  # Prevent duplicates
                        town_count += 1

            # Update the report for the current file
            if town_count > 0:  # ✅ Only store if new towns were added
                file_key = f"{governorate} - {city}"
                report[file_key] = town_count

    # Step 3: Append new data to CSV
    with open(output_file, "a", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write header if the file is newly created
        if os.stat(output_file).st_size == 0:
            writer.writerow(["Governorate", "City", "District", "Town"])

        # Write only new data
        writer.writerows(data)

    print(f"Processing completed. {len(data)} new rows added to {output_file}")

    if report:
        print("\nReport: Number of new towns added per file:")
        for key, count in report.items():
            print(f"{translate(key)}: {count} new towns")

    return report


if __name__ == "__main__":
    input_dir = "./سوريا"
    output_file = "syrian_towns.csv"
    report = parse_directory_and_generate_csv(input_dir, output_file)
