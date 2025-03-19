import pandas as pd
import os

# Paths to CSV files
data_dir = "/home/manu/skincare_recommendation/data"
products_path = os.path.join(data_dir, "products_cleaned.csv")
ingredients_path = os.path.join(data_dir, "ingredients_cleaned.csv")

# Load datasets
products = pd.read_csv(products_path)
ingredients = pd.read_csv(ingredients_path)

# 1️⃣ Handle Missing Prices
products["price_(kes)"] = products["price_(kes)"].fillna(products["price_(kes)"].median())

# 2️⃣ Feature Engineering: Extract Ingredient Benefits
ingredient_benefits = ingredients.set_index("ingredient")["benefit"].to_dict()

def extract_benefits(ingredient_list):
    """Convert ingredient list into associated benefits."""
    if pd.isna(ingredient_list):
        return []
    benefits = set()
    for ing in ingredient_list.split("; "):
        if ing in ingredient_benefits:
            benefits.add(ingredient_benefits[ing])
    return list(benefits)

products["benefits"] = products["ingredients"].apply(extract_benefits)

# 3️⃣ One-Hot Encoding for Skin Type & Conditions
products = products.join(products["skin_type"].str.get_dummies(sep="; ").add_prefix("skin_type_"))
products = products.join(products["conditions"].str.get_dummies(sep="; ").add_prefix("condition_"))

# 4️⃣ Save Processed Data
final_products_path = os.path.join(data_dir, "products_final.csv")
products.to_csv(final_products_path, index=False)

print(f"✅ Feature Engineering Completed! Final dataset saved as {final_products_path}")
print(products.head())

