from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum
import pandas as pd
import ast

app = FastAPI()

# Enable CORS (Allow requests from the frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend URL in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Load the dataset
file_path = "data/products_final.csv"
df = pd.read_csv(file_path)


# **1️⃣ Enum for Dropdown Options in Swagger UI**
class SkinType(str, Enum):
    Oily = "Oily"
    Dry = "Dry"
    Normal = "Normal"
    Combination = "Combination"
    Sensitive = "Sensitive"


class SkinCondition(str, Enum):
    Acne = "Acne"
    Eczema = "Eczema"
    Psoriasis = "Psoriasis"
    DrySkin = "Dry Skin"
    DiabeticSkin = "Diabetic Skin"
    Vitiligo = "Vitiligo"


# **2️⃣ Request Body Model with Swagger UI Enhancements**
class RecommendationRequest(BaseModel):
    skin_type: SkinType  # Dropdown for skin types
    conditions: list[SkinCondition]  # Multi-select dropdown


@app.get("/")
def root():
    return {"message": "Welcome to the Skincare Recommendation API"}


# **Helper Function to Handle Benefits Safely**
def safe_eval(value):
    try:
        return ast.literal_eval(value) if value.startswith("[") and value.endswith("]") else [value]
    except (SyntaxError, ValueError):
        return [value]  # Return as a list with a single item


# **3️⃣ Updated API Endpoint with UI Improvements**
@app.post("/recommend")
async def recommend(request: RecommendationRequest):
    # Convert Enum values to string
    skin_type = request.skin_type.value
    conditions = [cond.value for cond in request.conditions]

    # Filter products matching both skin type and conditions
    exact_match = df[
        df["skin_type"].str.contains(skin_type, case=False, na=False) &
        df["conditions"].apply(lambda x: any(cond in x for cond in conditions))
    ]

    # **Fallback Mechanism**
    if exact_match.empty:
        skin_type_match = df[df["skin_type"].str.contains(skin_type, case=False, na=False)]
        condition_match = df[df["conditions"].apply(lambda x: any(cond in x for cond in conditions))]
        fallback_recommendations = pd.concat([skin_type_match, condition_match]).drop_duplicates()

        if not fallback_recommendations.empty:
            exact_match = fallback_recommendations
        else:
            exact_match = df[df["skin_type"].str.contains("All", case=False, na=False)]

    # **Format JSON Response Properly**
    recommendations = []
    for _, row in exact_match.iterrows():
        benefits = safe_eval(row["benefits"]) if isinstance(row["benefits"], str) else row["benefits"]

        recommendations.append({
            "product_name": row["product_name"],
            "price_kes": row["price_(kes)"],
            "benefits": benefits
        })

    return {"recommended_products": recommendations}
