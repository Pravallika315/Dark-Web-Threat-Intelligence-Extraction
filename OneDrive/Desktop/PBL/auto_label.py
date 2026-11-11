import pandas as pd
import re

# Load the 200-record labeling template
df = pd.read_csv(
    "Dataset/threat_labeling_template.csv"
)

# Threat detection patterns
patterns = {
    "Ransomware": [
        r"\bransomware\b",
        r"\bransom demand\b",
        r"\bencrypted files\b",
        r"\bdecrypt files\b"
    ],

    "Credential Theft": [
        r"\bstolen credentials\b",
        r"\bstolen passwords\b",
        r"\bstolen login\b",
        r"\bpassword dump\b",
        r"\bcredential dump\b"
    ],

    "Phishing": [
        r"\bphishing\b",
        r"\bphishing campaign\b",
        r"\bfake login page\b",
        r"\bcredential harvesting\b"
    ],

    "Data Breach": [
        r"\bdata breach\b",
        r"\bstolen database\b",
        r"\bleaked database\b",
        r"\bexposed user data\b"
    ],

    "DDoS": [
        r"\bddos attack\b",
        r"\bdenial of service\b",
        r"\bbotnet attack\b"
    ],

    "Malware": [
        r"\bmalware\b",
        r"\btrojan\b",
        r"\bspyware\b",
        r"\bkeylogger\b",
        r"\bremote access trojan\b"
    ],

    "Vulnerability": [
        r"\bcve-\d{4}-\d+\b",
        r"\bzero day vulnerability\b",
        r"\bsecurity vulnerability\b",
        r"\bsoftware vulnerability\b"
    ]
}


def suggest_label(text):

    text = str(text).lower()

    matches = []

    for category, keywords in patterns.items():

        for keyword in keywords:

            if re.search(keyword, text):
                matches.append(category)
                break

    if len(matches) == 1:

        return matches[0], "Medium", "Review suggestion"

    elif len(matches) > 1:

        return (
            "Multiple Threats",
            "Medium",
            ", ".join(matches)
        )

    return (
        "Needs Review",
        "Low",
        "No clear threat pattern found"
    )


# Generate suggestions
suggestions = df["combined_text"].apply(
    suggest_label
)

df["suggested_label"] = suggestions.apply(
    lambda x: x[0]
)

df["confidence"] = suggestions.apply(
    lambda x: x[1]
)

df["reason"] = suggestions.apply(
    lambda x: x[2]
)

# Add review column
df["review_required"] = "Yes"

# Keep the manual label column
df["threat_label"] = ""

# Save a separate output file
df.to_csv(
    "Dataset/threat_label_suggestions.csv",
    index=False
)

print("\nAutomatic label suggestions completed!")

print("\nSuggested Label Distribution:")
print(df["suggested_label"].value_counts())

print("\nReview required for all records.")

print(
    "\nSaved: Dataset/threat_label_suggestions.csv"
)