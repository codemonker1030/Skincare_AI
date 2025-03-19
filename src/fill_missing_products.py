import pandas as pd

# Load existing products
file_path = "data/products_final.csv"  # Adjust if needed
df = pd.read_csv(file_path)

# Define all skin types and conditions
skin_types = ["Oily", "Dry", "Normal", "Combination", "Sensitive"]
conditions = ["Acne", "Eczema", "Psoriasis", "Dry Skin", "Diabetic Skin", "Vitiligo", "Blackheads", "Wrinkles"]

# Create a set of existing skin type-condition pairs
existing_pairs = set()
for _, row in df.iterrows():
    skin_list = str(row["skin_type"]).split("; ")
    condition_list = str(row["conditions"]).split("; ")
    for skin in skin_list:
        for condition in condition_list:
            existing_pairs.add((skin.strip(), condition.strip()))

# Generate missing products
new_rows = []
for skin in skin_types:
    for condition in conditions:
        if (skin, condition) not in existing_pairs:
            new_rows.append({
                "product_name": f"Generic {condition} Treatment for {skin} Skin",
                "price_(kes)": 2000,
                "skin_type": skin,
                "conditions": condition,
                "ingredients": "Generic Ingredients",
                "effectiveness_score": 7.5,
                "benefits": f"Helps manage {condition} for {skin} skin"
            })

# Add new rows to DataFrame and save
if new_rows:
    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    df.to_csv(file_path, index=False)
    print(f"✅ Added {len(new_rows)} missing products!")
else:
    print("✅ No missing products found!")
