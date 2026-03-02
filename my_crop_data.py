import pandas as pd

# Crop info
CROP_DATA = {
    "Rice": {"info": "Staple food crop, needs high rainfall."},
    "Wheat": {"info": "Cool-season crop, requires moderate rainfall."},
    "Maize": {"info": "Used for food, fodder, and industry."},
    "Sugarcane": {"info": "Cash crop, high water requirement."},
    "Millets": {"info": "Drought-resistant, suited for dry regions."}
}

# States & districts
INDIAN_STATES = {
    "Karnataka": ["Bagalkot","Bangalore Rural","Bangalore Urban"],
    "Andhra Pradesh": ["Anantapur","Chittoor","Guntur"],
    "Tamil Nadu": ["Chennai","Coimbatore","Madurai"],
    "Telangana": ["Hyderabad","Karimnagar","Warangal"],
    "Goa": ["North Goa","South Goa"],
    "Kerala": ["Thiruvananthapuram","Kochi","Kozhikode"]
}

# Crops per state
CROP_OPTIONS = {
    "Karnataka": ["Wheat","Maize","Rice"],
    "Andhra Pradesh": ["Rice","Maize","Chili"],
    "Tamil Nadu": ["Rice","Sugarcane","Cotton"],
    "Telangana": ["Rice","Cotton","Maize"],
    "Goa": ["Rice","Coconut","Vegetables"],
    "Kerala": ["Rice","Coconut","Banana"]
}

# Load CSV
def load_crop_yield_data(filepath="data/crop_yield.csv"):
    df = pd.read_csv(filepath)
    return df

# Average yield
def average_yield_per_crop(df):
    return df.groupby("Crop")["Yield"].mean().to_dict()
