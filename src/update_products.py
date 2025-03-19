import pandas as pd

# Load existing dataset
file_path = "/home/manu/skincare_recommendation/data/products_final.csv"
df = pd.read_csv(file_path)

# Define all possible skin types and concerns from `recommend.py`
all_skin_types = ["All", "Oily", "Dry", "Normal", "Combination", "Sensitive"]
all_concerns = ["Acne", "Eczema", "Psoriasis", "Dry Skin", "Diabetic Skin", "Vitiligo", "Blackheads", "Wrinkles"]

# ✅ Ensure all skin types & conditions exist in the dataset
for skin in all_skin_types:
    column_name = f"skin_type_{skin}"
    if column_name not in df.columns:
        df[column_name] = 0  # Add missing column and set default to 0

for condition in all_concerns:
    column_name = f"condition_{condition}"
    if column_name not in df.columns:
        df[column_name] = 0  # Add missing column and set default to 0

# ✅ Ensure "Diabetic Skin" is added to appropriate products
for index, row in df.iterrows():
    if "Dry Skin" in row["conditions"]:  # Diabetic skin needs extra hydration
        df.at[index, "conditions"] += "; Diabetic Skin"
        df.at[index, "condition_Diabetic Skin"] = 1

# ✅ Add new products for missing categories
new_products = [
    {
        "product_name": "Diabetic Skin Relief Lotion",
        "price_(kes)": 2500,
        "skin_type": "Dry",
        "conditions": "Diabetic Skin",
        "ingredients": "Shea Butter; Urea",
        "effectiveness_score": 8.8,
        "benefits": "['Deep hydration for diabetic skin']",
        "skin_type_Dry": 1, "skin_type_Sensitive": 0, "skin_type_Oily": 0, "skin_type_Normal": 0, "skin_type_Combination": 0, "skin_type_All": 0,
        "condition_Diabetic Skin": 1, "condition_Acne": 0, "condition_Eczema": 0, "condition_Psoriasis": 0, "condition_Vitiligo": 0, "condition_Blackheads": 0, "condition_Wrinkles": 0
    },
    {
        "product_name": "Gentle Exfoliating Scrub",
        "price_(kes)": 1700,
        "skin_type": "Combination; Normal",
        "conditions": "Blackheads",
        "ingredients": "Jojoba Beads; Glycolic Acid",
        "effectiveness_score": 8.6,
        "benefits": "['Removes dead skin, unclogs pores']",
        "skin_type_Dry": 0, "skin_type_Sensitive": 0, "skin_type_Oily": 0, "skin_type_Normal": 1, "skin_type_Combination": 1, "skin_type_All": 0,
        "condition_Diabetic Skin": 0, "condition_Acne": 0, "condition_Eczema": 0, "condition_Psoriasis": 0, "condition_Vitiligo": 0, "condition_Blackheads": 1, "condition_Wrinkles": 0
    }
]

# Convert new products to DataFrame and append
df_new = pd.DataFrame(new_products)
df_updated = pd.concat([df, df_new], ignore_index=True)

# ✅ Save the updated dataset
df_updated.to_csv(file_path, index=False)
print("✅ Dataset updated successfully!")
