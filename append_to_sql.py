import os

import mysql.connector
from deep_translator import GoogleTranslator

db_config = {
    "host": "localhost",
    "user": "your_username",
    "password": "your_password",
    "database": "SyriaData",
}


def translate(text):
    """Translate Arabic text to English using GoogleTranslator."""
    try:
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def get_or_create(
    cursor, table, column, value, additional_column=None, additional_value=None
):
    """Checks if a record exists in the given table and returns the ID. If not, inserts a new record."""
    if additional_column and additional_value:
        cursor.execute(
            f"SELECT id FROM {table} WHERE {column} = %s AND {additional_column} = %s",
            (value, additional_value),
        )
    else:
        cursor.execute(f"SELECT id FROM {table} WHERE {column} = %s", (value,))

    result = cursor.fetchone()

    if result:
        return result[0]  # ✅ Return existing ID (No duplicate insert)

    # ✅ Insert new record if not found
    if additional_column and additional_value:
        cursor.execute(
            f"INSERT INTO {table} ({column}, {additional_column}) VALUES (%s, %s)",
            (value, additional_value),
        )
    else:
        cursor.execute(f"INSERT INTO {table} ({column}) VALUES (%s)", (value,))

    return cursor.lastrowid  # ✅ Return newly created ID


def parse_directory_and_store_in_mysql(input_dir):
    """
    Parses directories for governorates, extracts cities, subdistricts, and towns,
    and stores them in the MySQL database.
    """
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    report = {}  # Stores the count of new towns per city

    for governorate_folder in os.listdir(input_dir):
        governorate_path = os.path.join(input_dir, governorate_folder)
        if not os.path.isdir(governorate_path):
            continue  # Skip non-directories

        for city_file in os.listdir(governorate_path):
            city_path = os.path.join(governorate_path, city_file)
            if not city_file.endswith(".txt"):
                continue  # Skip non-text files

            # Read file contents
            with open(city_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Extract governorate and city
            governorate = governorate_folder.strip()
            city = os.path.splitext(city_file)[0].strip()
            subdistrict = ""
            town_count = 0  # Count of new towns

            # ✅ Get or create Governorate
            governorate_id = get_or_create(cursor, "Governorate", "name", governorate)

            # ✅ Get or create City
            city_id = get_or_create(
                cursor, "City", "name", city, "governorate_id", governorate_id
            )

            for line in lines:
                stripped = line.strip()

                # ✅ Detect subdistrict
                if stripped.startswith("بلدات وقرى ناحية"):
                    subdistrict = stripped.replace("بلدات وقرى ناحية", "").strip()

                # ✅ Detect town and check if it exists
                elif stripped and not stripped.startswith("بلدات وقرى ناحية"):
                    district_id = get_or_create(
                        cursor, "District", "name", subdistrict, "city_id", city_id
                    )

                    # ✅ Check if the town already exists before inserting
                    cursor.execute(
                        "SELECT id FROM Town WHERE name = %s AND district_id = %s",
                        (stripped, district_id),
                    )
                    if cursor.fetchone():
                        continue  # ❌ Skip duplicate entry

                    cursor.execute(
                        "INSERT INTO Town (name, district_id) VALUES (%s, %s)",
                        (stripped, district_id),
                    )
                    town_id = cursor.lastrowid  # Store new town ID
                    print(f"Inserted town ID: {town_id} for town: {stripped}")

                    town_count += 1

            # ✅ Update the report
            if town_count > 0:  # ✅ Only include non-zero town counts
                file_key = f"{governorate} - {city}"
                report[file_key] = town_count

    connection.commit()
    cursor.close()
    connection.close()

    print("Processing completed. New data added to MySQL database.")

    if report:
        print("\nReport: Number of new towns added per file:")
        for key, count in report.items():
            print(f"{translate(key)}: {count} new towns")

    return report


if __name__ == "__main__":
    input_dir = "./سوريا"
    report = parse_directory_and_store_in_mysql(input_dir)
