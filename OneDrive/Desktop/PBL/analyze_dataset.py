
import pandas as pd
import json

from nlp_processor import analyze_text

# Load cleaned dataset
df = pd.read_csv(
    "Dataset/cleaned_dark_web_data.csv"
)

print("Starting NLP analysis...")
print("Total records:", len(df))

results = []

# Process each record
for index, row in enumerate(
    df.itertuples(index=False), start=1
):

    text = str(row.combined_text)

    try:
        result = analyze_text(text)

        results.append({

            "id": row.id,

            "title": row.title,

            "category": row.category,

            "created_at": row.created_at,

            "tokens": json.dumps(result["tokens"]),

            "entities": json.dumps(result["entities"]),

            "iocs": json.dumps(result["iocs"]),

            "threats": json.dumps(result["threats"]),

            "risk": result["risk"],

            "full_text": text

        })

    except Exception as e:

        print(f"Error in record {index}: {e}")

    # Display progress
    if index % 100 == 0:
        print(f"Processed {index}/{len(df)} records")

# Convert results into DataFrame
result_df = pd.DataFrame(results)

# Save output
result_df.to_csv(
    "Dataset/threat_analysis_results.csv",
    index=False
)

print("\nNLP Analysis Completed!")

print("Successfully processed:", len(result_df))

print("\nThreat Distribution:")

print(
    result_df["threats"].value_counts().head(15)
)

print("\nRisk Distribution:")

print(result_df["risk"].value_counts())

print("\nSaved: Dataset/threat_analysis_results.csv")
