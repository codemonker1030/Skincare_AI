import pandas as pd

# Load the dataset
df = pd.read_csv("/home/manu/skincare_recommendation/data/products_final.csv")

# Fill missing values in 'conditions' with "Unknown"
df['conditions'] = df['conditions'].fillna("Unknown")

# Save the cleaned dataset
df.to_csv("/home/manu/skincare_recommendation/data/products_final.csv", index=False)

print("\n✅ Missing values fixed! Updated dataset saved.")
print("\n✅ First 5 Rows of the Updated Dataset:")
print(df.head())
