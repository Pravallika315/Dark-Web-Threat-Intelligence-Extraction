
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Load cleaned dataset
df = pd.read_csv(
    "Dataset/cleaned_dark_web_data.csv"
)

# Prepare text
documents = df["combined_text"].fillna("").astype(str)

# Convert text into numerical features
vectorizer = CountVectorizer(
    max_df=0.95,
    min_df=5,
    stop_words="english",
    max_features=3000,
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(documents)

# Create LDA model
lda = LatentDirichletAllocation(
    n_components=8,
    random_state=42,
    max_iter=10,
    learning_method="batch"
)

# Train model
lda.fit(X)

# Get feature names
words = vectorizer.get_feature_names_out()

# Display discovered topics
print("\n========== DISCOVERED TOPICS ==========")

for topic_index, topic in enumerate(lda.components_):

    top_words = topic.argsort()[-10:][::-1]

    keywords = [
        words[index] for index in top_words
    ]

    print(f"\nTopic {topic_index + 1}:")
    print(", ".join(keywords))

# Assign dominant topic to each document
topic_distribution = lda.transform(X)

df["topic_id"] = topic_distribution.argmax(axis=1) + 1

df["topic_probability"] = topic_distribution.max(axis=1)

# Save results
df.to_csv(
    "Dataset/topic_modeling_results.csv",
    index=False
)

print("\nTopic modelling completed!")
print("Total topics:", lda.n_components)

print("\nDocument distribution:")
print(df["topic_id"].value_counts().sort_index())

print("\nSaved: Dataset/topic_modeling_results.csv")
