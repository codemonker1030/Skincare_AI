import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the cleaned dataset
df = pd.read_csv("data/products_final.csv")  # Correct file path


# Combine relevant text columns for recommendation
df["combined_features"] = df["skin_type"].fillna("") + " " + df["conditions"].fillna("") + " " + df["ingredients"].fillna("")

# Convert text data to numerical features using TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
feature_matrix = vectorizer.fit_transform(df["combined_features"])

# Compute similarity scores (cosine similarity)
similarity_matrix = cosine_similarity(feature_matrix, feature_matrix)

# Save the trained model and vectorizer
with open("models/recommendation.pkl", "wb") as model_file:

    pickle.dump((df, similarity_matrix, vectorizer), model_file)

print("✅ Training Completed! Model saved as recommendation.pkl")
