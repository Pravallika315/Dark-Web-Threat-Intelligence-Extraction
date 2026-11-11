
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load dataset
df = pd.read_csv(
    "Dataset/cleaned_dark_web_data.csv"
)

# Remove records with unknown categories
df = df[df["category"] != "Unknown"].copy()

# Remove categories with fewer than 20 samples
counts = df["category"].value_counts()

valid_categories = counts[counts >= 20].index

df = df[df["category"].isin(valid_categories)]

# Input and output
X = df["combined_text"].fillna("")
y = df["category"]

print("Training records:", len(df))
print("Number of categories:", y.nunique())

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Convert text into TF-IDF features
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english",
    ngram_range=(1, 2),
    min_df=2
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train Logistic Regression
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train_tfidf, y_train)

# Predictions
predictions = model.predict(X_test_tfidf)

# Evaluation
accuracy = accuracy_score(y_test, predictions)

print("\nModel Training Completed!")

print("\nAccuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

print("\nConfusion Matrix:")

print(confusion_matrix(
    y_test,
    predictions
))

# Save predictions
output = pd.DataFrame({
    "actual_category": y_test.values,
    "predicted_category": predictions
})

output.to_csv(
    "Dataset/category_predictions.csv",
    index=False
)

print("\nPredictions saved successfully!")
# Save trained model
os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/category_model.pkl"
)

joblib.dump(
    vectorizer,
    "models/tfidf_vectorizer.pkl"
)

print("\nModel saved successfully!")
print("Saved: models/category_model.pkl")
print("Saved: models/tfidf_vectorizer.pkl")