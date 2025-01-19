# Syria Administrative Data Processing

## Overview
This project processes **Syria's administrative divisions** by extracting and storing data from text files into **MySQL** and **CSV formats**. The data includes:
- **Governorates** (المحافظة)
- **Cities** (المدينة)
- **Districts** (الناحية)
- **Towns** (البلدة)

The scripts ensure **no duplicate entries** and support **automatic translation** of Arabic names to English.

---

## 📂 Project Structure
```
.
├── append_to_csv.py       # Extracts data and appends it to a CSV file
├── append_to_sql.py       # Extracts data and stores it in a MySQL database
├── data.txt               # Sample input data
├── output.txt             # Sample output data
├── required.sql           # SQL script to create MySQL tables and views
├── requirements.txt       # List of required Python packages
└── سوريا/                # Folder containing text files for each governorate
    ├── محافظة إدلب/
    │   ├── ادلب.txt
    │   ├── اريحا.txt
    │   ├── جسر الشغور.txt
    │   ├── حارم.txt
    │   └── معرة النعمان.txt
    ├── محافظة حلب/
    │   ├── أعزاز.txt
    │   ├── الباب.txt
    │   ├── جرابلس.txt
    │   └── منبج.txt
    └── ... (other governorates and their cities)
```

---

## 🛠️ Setup Instructions

### 1️⃣ Install Dependencies
Ensure you have Python and MySQL installed, then install required Python packages:
```sh
pip install -r requirements.txt
```

### 2️⃣ Set Up MySQL Database
Run the following SQL script (`required.sql`) in **MySQL Workbench** to create the necessary database and tables:
```sh
mysql -u root -p < required.sql
```

### 3️⃣ Update MySQL Credentials
Modify the `db_config` dictionary in **`append_to_sql.py`** to match your MySQL credentials:
```python
db_config = {
    "host": "localhost",
    "user": "your_username",
    "password": "your_password",
    "database": "SyriaData",
}
```

### 4️⃣ Run Data Processing Scripts
#### **Option 1: Store Data in MySQL**
```sh
python append_to_sql.py
```
This script:
- Reads text files
- Extracts governorates, cities, districts, and towns
- **Inserts data into MySQL while avoiding duplicates**

#### **Option 2: Store Data in CSV**
```sh
python append_to_csv.py
```
This script:
- Reads text files
- Extracts governorates, cities, districts, and towns
- **Appends new entries to a CSV file (`syrian_towns.csv`)**

---

## 🗄️ Database Schema
### **Tables Created in MySQL**
```sql
CREATE TABLE Governorate (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE City (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    governorate_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (governorate_id) REFERENCES Governorate(id) ON DELETE CASCADE,
    UNIQUE (name, governorate_id)
);

CREATE TABLE District (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (city_id) REFERENCES City(id) ON DELETE CASCADE,
    UNIQUE (name, city_id)
);

CREATE TABLE Town (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    district_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (district_id) REFERENCES District(id) ON DELETE CASCADE,
    UNIQUE (name, district_id)
);
```

### **Database View for Easy Querying**
To view all data in a single query, use the provided SQL view:
```sql
CREATE VIEW SyriaLocationView AS
SELECT
    g.name AS Governorate,
    c.name AS City,
    d.name AS District,
    t.name AS Town
FROM Town t
JOIN District d ON t.district_id = d.id
JOIN City c ON d.city_id = c.id
JOIN Governorate g ON c.governorate_id = g.id;
```
You can retrieve all data with:
```sql
SELECT * FROM SyriaLocationView;
```

---

## 📌 Features
✔ **Extracts data from structured text files**
✔ **Prevents duplicate data entries**
✔ **Stores data in MySQL and CSV formats**
✔ **Supports Arabic-English translation**
✔ **Provides an SQL View for easier queries**

---

## 🔍 Example Output
#### **Sample MySQL Query Output**
```plaintext
+------------------+------------+----------------+-----------+
| Governorate      | City       | District       | Town      |
+------------------+------------+----------------+-----------+
| محافظة دمشق    | دمشق       | حي الميدان     | الدقاق  |
| محافظة السويداء | السويداء   | مركز السويداء  | الأصلحا  |
+------------------+------------+----------------+-----------+
```

#### **Sample CSV Output (`syrian_towns.csv`)**
```csv
Governorate,City,District,Town
محافظة دمشق,دمشق,حي الميدان,القنوات
محافظة السويداء,السويداء,مركز السويداء,الأصلحا
```

---

## 📧 Contact & Contributions
Feel free to contribute to this project! If you have questions, open an issue or reach out. 😊

**Author:** Mohammad KaraBala

