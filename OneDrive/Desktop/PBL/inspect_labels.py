
import pandas as pd

# Load reviewed labels
df = pd.read_csv(
    "Dataset/threat_labeled_data_reviewed.csv"
)

print("Total records:", len(df))

print("\nThreat Label Distribution:")
print(df["threat_label"].value_counts())

# Separate reviewed and unreviewed records
reviewed = df[
    df["threat_label"] != "Needs Review"
]

pending = df[
    df["threat_label"] == "Needs Review"
]

print("\nReviewed records:", len(reviewed))
print("Pending review:", len(pending))

print("\nRecords available per class:")

print(
    reviewed["threat_label"].value_counts()
)

# Save reviewed data separately
reviewed.to_csv(
    "Dataset/verified_training_data.csv",
    index=False
)

print("\nSaved: Dataset/verified_training_data.csv")
