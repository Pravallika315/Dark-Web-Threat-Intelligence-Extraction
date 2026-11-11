
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "threat_intelligence.db"

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)

# CSV files to import
files = {
    "threat_analysis": "Dataset/threat_analysis_results.csv",
    "topic_analysis": "Dataset/topic_modeling_results.csv",
    "category_predictions": "Dataset/category_predictions.csv"
}

# Import each CSV into SQLite
for table_name, file_path in files.items():

    if Path(file_path).exists():

        df = pd.read_csv(file_path)

        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        print(
            f"{table_name}: {len(df)} records imported"
        )

    else:
        print(f"File not found: {file_path}")

# Display database tables
cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
)

print("\nDatabase Tables:")

for table in cursor.fetchall():
    print(table[0])

conn.close()

print("\nDatabase created successfully!")
print("Saved as:", DB_PATH)
