import pandas as pd
import random
import os

# Output file
OUTPUT_FILE = "crop_data.csv"

# Possible values
states = ["Karnataka", "AP", "TN", "MP", "Telangana", "Kerala", "Goa"]
districts = {
    "Karnataka": ["Bangalore", "Mysore", "Mangalore"],
    "AP": ["Vijayawada", "Guntur", "Tirupati"],
    "TN": ["Chennai", "Coimbatore", "Madurai"],
    "MP": ["Indore", "Bhopal", "Jabalpur"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode"],
    "Goa": ["Panaji", "Margao"]
}
crops = ["Wheat", "Rice", "Ragi", "Maize", "Cotton", "Sugarcane"]

rows = []

# Generate 100 rows
for _ in range(100):
    state = random.choice(states)
    district = random.choice(districts[state])
    crop = random.choice(crops)
    area = round(random.uniform(500, 2000), 2)          # hectares
    production = round(area * random.uniform(1.5, 3.0), 2)  # tonnes
    rainfall = round(random.uniform(700, 1200), 2)      # mm/year
    fertilizer = round(random.uniform(50, 200), 2)      # kg/ha
    pesticide = round(random.uniform(5, 20), 2)         # kg/ha
    yield_val = round(production / area, 2)             # simplistic yield = prod / area
    rows.append([state, district, crop, area, production, rainfall, fertilizer, pesticide, yield_val])

# Create DataFrame
df = pd.DataFrame(rows, columns=["State", "District", "Crop", "Area", "Production", "Rainfall", "Fertilizer", "Pesticide", "Yield"])

# Save CSV
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ {OUTPUT_FILE} generated with {len(df)} rows.")
