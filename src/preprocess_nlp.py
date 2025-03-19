import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import string

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# Function to clean text
def clean_text(text):
    if isinstance(text, str):
        text = text.lower()  # Convert to lowercase
        text = text.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
        words = text.split()
        words = [word for word in words if word not in stop_words]  # Remove stopwords
        return " ".join(words)
    return ""

# Load dataset
df = pd.read_csv("data/products_final.csv")

# Apply text cleaning
df["cleaned_benefits"] = df["benefits"].apply(clean_text)
df["cleaned_ingredients"] = df["ingredients"].apply(clean_text)

# Save the cleaned dataset
df.to_csv("data/products_cleaned.csv", index=False)

print("✅ Text preprocessing complete. Cleaned data saved as 'products_cleaned.csv'.")
