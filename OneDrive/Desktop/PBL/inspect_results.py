
import pandas as pd
import json

df = pd.read_csv(
    "Dataset/threat_analysis_results.csv"
)

print("TOTAL RECORDS:", len(df))

# Show detected threat examples
print("\n========== DETECTED THREATS ==========")

detected = df[
    df["threats"].apply(
        lambda x: "Unclassified" not in json.loads(x)
    )
]

for _, row in detected.head(10).iterrows():

    print("\nTitle:", row["title"])
    print("Category:", row["category"])
    print("Threats:", row["threats"])
    print("Risk:", row["risk"])
    print("Text:", str(row["full_text"])[:300])

# Show unclassified examples
print("\n========== UNCLASSIFIED SAMPLES ==========")

unclassified = df[
    df["threats"].apply(
        lambda x: json.loads(x) == ["Unclassified"]
    )
]

for _, row in unclassified.head(10).iterrows():

    print("\nTitle:", row["title"])
    print("Category:", row["category"])
    print("Text:", str(row["full_text"])[:300])

print("\nInspection completed!")
