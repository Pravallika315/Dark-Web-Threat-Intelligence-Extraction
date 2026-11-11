
import pandas as pd

df = pd.read_csv(
    "Dataset/verified_training_data.csv"
)

print("DATASET SUMMARY")
print("====================")

print("Total records:", len(df))

print("\nLabel distribution:")

print(df["threat_label"].value_counts())

print("\nThreat vs Benign:")

df["binary_label"] = df["threat_label"].apply(
    lambda x: "Benign"
    if x == "Benign"
    else "Threat"
)

print(df["binary_label"].value_counts())

print("\nDataset inspection completed!")
