
import pandas as pd

# Load cleaned dataset
df = pd.read_csv(
    "Dataset/cleaned_dark_web_data.csv"
)

# Select useful columns
df = df[[
    "id",
    "title",
    "category",
    "combined_text"
]].copy()

# Select 200 random records for manual labeling
sample = df.sample(
    n=min(200, len(df)),
    random_state=42
)

# Add manual label column
sample["threat_label"] = ""

# Save labeling template
sample.to_csv(
    "Dataset/threat_labeling_template.csv",
    index=False
)

print("Threat labeling template created!")
print("Records to review:", len(sample))

print(
    "\nSaved: Dataset/threat_labeling_template.csv"
)
