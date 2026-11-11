
import pandas as pd
from pathlib import Path

# Dataset location
file_path = Path("Dataset/base_dark_final.csv")

# Load dataset
df = pd.read_csv(file_path)

print("Original Dataset Shape:", df.shape)

# Remove unnecessary index columns
df = df.loc[
    :, ~df.columns.str.contains("^Unnamed")
]

# Handle missing values
df["title"] = df["title"].fillna("")
df["full_text"] = df["full_text"].fillna("")
df["category"] = df["category"].fillna("Unknown")

# Convert probability into numeric format
if "probability" in df.columns:
    df["probability"] = pd.to_numeric(
        df["probability"], errors="coerce"
    )

# Combine title and content
df["combined_text"] = (
    df["title"].astype(str) + " " +
    df["full_text"].astype(str)
).str.strip()

# Remove empty text records
df = df[df["combined_text"] != ""]

# Remove duplicate text records
df = df.drop_duplicates(
    subset=["combined_text"]
)

# Reset index
df = df.reset_index(drop=True)

# Save cleaned dataset
output_path = Path(
    "Dataset/cleaned_dark_web_data.csv"
)

df.to_csv(output_path, index=False)

# Display results
print("\nPreprocessing completed!")
print("Final Dataset Shape:", df.shape)
print("\nAvailable Columns:")
print(df.columns.tolist())

print("\nCategory Distribution:")
print(df["category"].value_counts())

print("\nSaved file:", output_path)
