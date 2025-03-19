import pandas as pd

# Load the dataset
file_path = "data/products_final.csv"
df = pd.read_csv(file_path)

# User Input
skin_types = ["Oily", "Dry", "Normal", "Combination", "Sensitive"]
conditions = ["Acne", "Eczema", "Psoriasis", "Dry Skin", "Diabetic Skin", "Vitiligo"]

# Ask for skin type
print("\n✅ Skin Type (Select One)")
for i, skin in enumerate(skin_types, 1):
    print(f"{i}. {skin}")
skin_choice = int(input("Enter the number corresponding to your skin type: "))
selected_skin_type = skin_types[skin_choice - 1]

# Ask for skin conditions
print("\n✅ Skin Conditions (Select All That Apply, comma-separated)")
for i, condition in enumerate(conditions, 1):
    print(f"{i}. {condition}")
condition_choices = input("Enter the numbers corresponding to your skin concerns (e.g., 1,3): ")
selected_conditions = [conditions[int(i) - 1] for i in condition_choices.split(",")]

# Filter products matching both skin type and conditions
exact_match = df[
    df["skin_type"].str.contains(selected_skin_type, case=False, na=False) &
    df["conditions"].apply(lambda x: any(cond in x for cond in selected_conditions))
]

# ** Fallback Mechanism **  
if exact_match.empty:
    print("\n⚠ No exact matches found! Showing closest recommendations...\n")
    
    # Find products that match at least the skin type
    skin_type_match = df[df["skin_type"].str.contains(selected_skin_type, case=False, na=False)]
    
    # Find products that match at least one condition
    condition_match = df[df["conditions"].apply(lambda x: any(cond in x for cond in selected_conditions))]
    
    # Merge results and remove duplicates
    fallback_recommendations = pd.concat([skin_type_match, condition_match]).drop_duplicates()
    
    if not fallback_recommendations.empty:
        exact_match = fallback_recommendations
    else:
        print("\n⚠ No close matches found! Showing general skincare products for all skin types.\n")
        exact_match = df[df["skin_type"].str.contains("All", case=False, na=False)]

# Display recommendations with Benefits
print("\n✅ Recommended Products:\n")
for _, row in exact_match.iterrows():
    print(f"- {row['product_name']} ({row['price_(kes)']} KES)")
    print(f"  🛠 Benefits: {row['benefits']}\n")
