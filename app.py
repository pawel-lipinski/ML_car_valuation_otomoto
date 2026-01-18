"""
Otomoto Car Valuation Engine (Production App)
---------------------------------------------
This Streamlit application serves as the frontend for the AutoGluon pricing model.
It captures 30+ vehicle features, handles missing data artifacts, and applies 
post-prediction business logic (brand bias adjustments) to ensure market-accurate pricing.

Author: AI Assistant / Project Lead
Date: 2026-01-17
Model Version: Production_v1 (WeightedEnsemble_L2)
"""

import streamlit as st
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import os
from typing import Optional, Dict, Any

# ==========================================
# 1. CONFIGURATION & CONSTANTS
# ==========================================

# Configure the browser tab title and layout
st.set_page_config(
    page_title="AI Car Valuator Pro", 
    page_icon="🏎️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Path to the AutoGluon model folder (exported via .clone_for_deployment())
MODEL_PATH = 'production_model'

# BUSINESS LOGIC LAYER
# Based on the Model Audit (Cell 9.6 in Notebook), we apply these corrections
# to fix known model biases (e.g., Underpricing reliable cars, Overpricing imports).
BRAND_ADJUSTMENTS: Dict[str, float] = {
    # Discount Overvalued Brands
    'Peugeot': 0.88,   # -12% correction
    'Citroën': 0.93,   # -7% correction
    'Renault': 0.94,   # -6% correction
    'Ford': 0.94,      # -6% (Corrects for US Salvage Imports)
    'Jeep': 0.96,      # -4% correction
    'RAM': 0.90,       # -10% (Heavy correction for niche imports)
    'Fiat': 0.95,      # -5% (Corrects for Camper Van outliers)
    
    # Premium for Undervalued Brands
    'Honda': 1.03,     # +3% (Reliability Premium)
    'Toyota': 1.02,    # +2% (Market Trust)
    'Porsche': 1.05,   # +5% (Collector/Investment Value)
    'Lexus': 1.04      # +4% (Reliability Premium)
}

# ==========================================
# 2. RESOURCE LOADING
# ==========================================

@st.cache_resource
def load_model() -> Optional[TabularPredictor]:
    """
    Loads the AutoGluon model from disk.
    Uses st.cache_resource to load only once per session to improve performance.
    
    Returns:
        TabularPredictor or None if path is invalid.
    """
    if not os.path.exists(MODEL_PATH):
        return None
    
    # Load model (verbosity=0 silences warnings in the UI)
    return TabularPredictor.load(MODEL_PATH, verbosity=0)

# Initialize the predictor
predictor = load_model()

# Extract dynamic brand list from model metadata if possible
# This ensures the dropdown matches exactly what the model learned.
if predictor:
    try:
        known_brands = sorted(predictor.feature_metadata_in.type_map_raw['brand'].categories)
    except Exception:
        # Fallback list if metadata extraction fails
        known_brands = ["Audi", "BMW", "Ford", "Opel", "Toyota", "Volkswagen", "Other"]
else:
    known_brands = []

# ==========================================
# 3. USER INTERFACE: SIDEBAR (Core Features)
# ==========================================

with st.sidebar:
    st.header("1. Basic Data")
    st.info("Start by defining the core vehicle identity.")
    
    # Core Identification
    brand = st.selectbox("Brand", known_brands, index=known_brands.index("Volkswagen") if "Volkswagen" in known_brands else 0)
    car_model = st.text_input("Model", value="Golf", help="e.g. Passat, X5, Focus")
    
    # Core Specs
    year = st.slider("Production Year", 1990, 2026, 2019)
    mileage = st.number_input("Mileage (km)", 0, 999999, 145000, step=1000)
    power = st.number_input("Horsepower (HP)", 40, 999, 150)
    fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Hybrid", "Electric", "LPG"])
    
    st.divider()
    
    st.header("2. Key Drivers")
    st.caption("These features significantly impact valuation.")
    
    # NOTE: Ensure these string values match the Training Data language (e.g. 'Manualna' vs 'Manual')
    gearbox = st.selectbox("Gearbox", ["Manual", "Automatic", "CVT", "Dual Clutch"])
    body_type = st.selectbox("Body Type", ["Sedan", "Compact", "SUV", "Station Wagon", "Coupe", "Cabriolet", "Minivan"])
    
    # Boolean Flags
    damaged = st.checkbox("Damaged / Wrecked?", value=False, help="Check this if the car has structural damage.")
    is_imported = st.checkbox("Imported Car?", value=True, help="Was this car imported from abroad?")

# ==========================================
# 4. USER INTERFACE: MAIN AREA (Details)
# ==========================================

st.title("🏎️ AI Car Valuator: Pro Mode")
st.markdown(f"### Pricing Engine Status: `{'🟢 Online' if predictor else '🔴 Offline'}`")
st.markdown("Enter detailed specifications below for the most accurate market prediction.")

# We use an Expander to hide complex/secondary features to keep the UI clean
with st.expander("📝 Step 3: Detailed Configuration (Granular Data)", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**History & Condition**")
        no_accident = st.checkbox("Accident Free", value=True)
        has_registration = st.checkbox("Registered in Poland", value=True)
        new_used = st.selectbox("Condition", ["Used", "New", "Demo"], index=0)
        country_origin = st.selectbox("Origin", ["Poland", "Germany", "France", "USA", "Other"], index=0)

    with col2:
        st.markdown("**Technical Specs**")
        engine_capacity = st.number_input("Capacity (cm3)", 500, 8000, 1968)
        transmission = st.selectbox("Drivetrain", ["Front Wheel", "Rear Wheel", "4x4"], index=0)
        door_count = st.number_input("Doors", 2, 5, 5)
        nr_seats = st.number_input("Seats", 2, 9, 5)
        color = st.text_input("Color", "Black")
        
    with col3:
        st.markdown("**Location & Trim**")
        city = st.text_input("City", "Warsaw")
        region = st.selectbox("Region", ["Mazowieckie", "Małopolskie", "Śląskie", "Wielkopolskie", "Other"])
        version = st.text_input("Trim Version", "", help="e.g. Highline, M-Sport, AMG Line")
        generation = st.text_input("Generation", "", help="e.g. VII, F30, W205")

# Hidden Advanced Technicals (User rarely knows these, so we provide smart defaults)
with st.expander("⚙️ Advanced Technicals (Defaults applied)"):
    c1, c2, c3 = st.columns(3)
    co2 = c1.number_input("CO2 (g/km)", 0, 500, 140)
    urban_cons = c2.number_input("Urban Consumption (l/100km)", 0.0, 30.0, 7.5)
    extra_urban_cons = c3.number_input("Highway Consumption (l/100km)", 0.0, 20.0, 5.5)

# ==========================================
# 5. PREDICTION ENGINE
# ==========================================

if st.button("🚀 Calculate Precise Value", type="primary", use_container_width=True):
    if not predictor:
        st.error(f"❌ Critical Error: Model not found at `{MODEL_PATH}`. Please check the folder.")
    else:
        # A. Data Construction
        # We must map the UI variables to the EXACT column names expected by the model.
        input_data = pd.DataFrame({
            # Primary Features
            'brand': [brand],
            'model': [car_model],
            'year': [year],
            'mileage': [mileage],
            'engine_power': [power],
            'fuel_type': [fuel],
            
            # Secondary Features
            'gearbox': [gearbox],
            'body_type': [body_type],
            'damaged': [damaged],
            'is_imported_car': [is_imported],
            
            # Detailed Features
            'no_accident': [no_accident],
            'has_registration': [has_registration],
            'new_used': [new_used],
            'country_origin': [country_origin],
            'engine_capacity': [engine_capacity],
            'transmission': [transmission], 
            'door_count': [door_count],
            'nr_seats': [nr_seats],
            'color': [color],
            'city': [city],
            'region': [region],
            'version': [version],
            'generation': [generation],
            
            # Advanced Features
            'co2_emissions': [co2],
            'urban_consumption': [urban_cons],
            'extra_urban_consumption': [extra_urban_cons],
            
            # Artifact Features (Required by model structure but not used for inference)
            # We pass defaults to prevent KeyError in the AutoML pipeline.
            'latitude': [52.2297],       # Default: Warsaw Latitude
            'price_currency': ['PLN'],   # Fixed
            'seller_since_year': [2020], # Neutral assumption
            'region_grid': [None]        # Nullable
        })

        # B. Execution
        try:
            with st.spinner('AI analyzing market trends...'):
                # 1. Get Base Prediction from AutoGluon
                raw_price = predictor.predict(input_data)[0]
                
                # 2. Apply Business Logic Adjustments
                # Fetch factor from dictionary, default to 1.0 (no change) if brand not listed
                adjustment_factor = BRAND_ADJUSTMENTS.get(brand, 1.0)
                final_price = raw_price * adjustment_factor
                
                # Calculate the monetary value of the adjustment
                diff = final_price - raw_price
            
            # C. Result Visualization
            st.divider()
            
            # Layout: Price on Left, Context on Right
            c_price, c_info = st.columns([1.5, 1])
            
            with c_price:
                st.metric(
                    label="🎯 Estimated Market Value", 
                    value=f"{final_price:,.0f} PLN",
                    help="Final price after AI prediction and Brand Bias correction."
                )
                
                # Show correction context if applicable
                if adjustment_factor != 1.0:
                    st.caption(
                        f"ℹ️ Includes a **{diff:+,.0f} PLN** correction based on "
                        f"{brand}'s historical market performance vs. technical specs."
                    )
            
            with c_info:
                # Buying Guide Logic
                lower_bound = final_price * 0.93
                upper_bound = final_price * 1.07
                
                st.success(f"**Great Deal:** < {lower_bound:,.0f} PLN")
                st.warning(f"**Fair Price:** {lower_bound:,.0f} - {upper_bound:,.0f} PLN")
                st.error(f"**Overpriced:** > {upper_bound:,.0f} PLN")

            # D. Debugging / Transparency (Optional)
            with st.expander("🔍 Developer Logs (JSON Input)"):
                st.write(f"Raw AI Output: {raw_price:,.2f}")
                st.write(f"Adjustment Factor: {adjustment_factor}x")
                st.json(input_data.to_dict(orient='records')[0])

        except Exception as e:
            st.error("⚠️ Prediction Failed")
            st.warning(f"Error Details: {e}")
            st.info("Hint: Check if 'Gearbox' or 'Body Type' values match the training data language (Polish/English).")