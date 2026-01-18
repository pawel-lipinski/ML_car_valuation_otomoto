# \# Otomoto Car Price Prediction Model (train data - DEC 2025)

# 

# \## Project Overview

# This project is an end-to-end Machine Learning pipeline designed to predict used car prices in the Polish market (Otomoto).

# 

# Unlike simple regression models, this system uses \*\*AutoGluon's "Best Quality" Multi-Layer Stacking\*\*, which ensembles Neural Networks, CatBoost, and LightGBM models to achieve state-of-the-art accuracy. It is specifically engineered to handle the complexities of the Polish market, including regional price differences, budget car anomalies, and luxury vehicle valuations.

# 

# \## Key Features

# 

# \### Model Architecture

# \* \*\*AutoGluon Stacking:\*\* Utilizes a multi-layer ensemble strategy (Stacking \& Bagging) rather than a single algorithm.

# \* \*\*Auto-Tuning:\*\* Automatically optimizes hyperparameters for maximum MAE (Mean Absolute Error) reduction.

# 

# \### Feature Engineering

# \* \*\*Automated Translation:\*\* Translates categorical features (Color, Body Type, Transmission) from Polish to English using `deep\_translator`.

# \* \*\*Geo-Spatial Intelligence:\*\* Calculates `dist\_to\_warsaw` (distance to capital) to account for regional purchasing power differences.

# \* \*\*Power-to-Weight Parsing:\*\* Extracts numeric data from messy string fields (e.g., "150 KM", "2000 cm3").

# 

# \### Robustness \& Safety

# \* \*\*"Shielded" Outlier Detection:\*\* A custom Isolation Forest implementation that removes statistical anomalies (e.g., a 10M PLN Volkswagen Golf) while "shielding" legitimate luxury cars (Ferrari, Lamborghini, AMG) from being deleted.

# \* \*\*Sanity Guard (Budget Segment):\*\* A post-prediction logic layer that prevents "hallucinations" in the under-30k PLN segment by capping predictions against historical market averages.

# 

# ---

# 

# \## Project Structure

# 

# ```text

# ├── data/

# │   ├── raw\_data.csv                  # Raw scraping data (Input)

# │   ├── train.csv                     # Cleaned training dataset

# │   └── test.csv                      # Holdout dataset (20%)

# │

# ├── saved\_models/                     # PRODUCTION ARTIFACTS (DEPLOY FROM HERE)

# │   ├── autogluon\_pro\_ensemble/       # The Champion Model (Contains model artifacts)

# │   └── feature\_columns.pkl           # Critical: List of column names/order required for prediction

# │

# ├── ag\_models\_benchmark/              # Temporary: Output from initial "Quick Shootout"

# ├── ag\_models\_pro/                    # Temporary: Working directory for heavy training

# │

# └── otomoto\_model\_training\_2026.ipynb # Main Training \& Audit Pipeline





Pipeline Workflow1. Data Ingestion \& CleaningThe notebook otomoto\_model\_training\_2026.ipynb loads raw data, parses numeric values, and handles missing data. It applies a Shielded Isolation Forest to remove corrupted records without losing high-value inventory.2. Training (AutoGluon Pro)We use the presets='best\_quality' configuration. This trains models in layers:Layer 1: CatBoost, XGBoost, Neural Net Torch, LightGBM.Layer 2: A meta-learner that combines the outputs of Layer 1 to correct their biases.3. Professional AuditThe pipeline includes a comprehensive auditing suite:Segmented Performance Matrix: Evaluates MAE/MAPE across Budget, Economy, Mid-Range, Premium, and Luxury tiers.Residual Analysis: Visualizes heteroscedasticity.Brand Bias Scorecard: Identifies if the model systematically overprices or underprices specific brands (e.g., Dacia vs. Porsche).The "Black Book": Automatically flags the top 5 worst over-valuations and under-valuations for manual review.Installation \& RequirementsEnsure you have the necessary Python libraries installed:Bashpip install pandas numpy matplotlib seaborn scikit-learn xgboost catboost shap deep-translator joblib autogluon

Note: CUDA (GPU) is recommended for training but not required for inference.How to Load \& Predict (Inference)To use the saved model in a production script, API, or web app (Streamlit/Flask):Pythonfrom autogluon.tabular import TabularPredictor

import pandas as pd

import pickle



\# 1. Load the Champion Model

\# Point to the folder inside 'saved\_models'

predictor = TabularPredictor.load("saved\_models/autogluon\_pro\_ensemble")



\# 2. Load Feature Definitions (Optional but Recommended)

\# Ensures you provide columns in the exact order the model expects

with open("saved\_models/feature\_columns.pkl", "rb") as f:

&nbsp;   feature\_cols = pickle.load(f)



\# 3. Prepare New Data

\# 'new\_data' must be a Pandas DataFrame matching the training schema

new\_data = pd.DataFrame({

&nbsp;   'year': \[2018],

&nbsp;   'mileage': \[120000],

&nbsp;   'brand': \['Audi'],

&nbsp;   'model': \['A4'],

&nbsp;   'fuel\_type': \['Diesel'],

&nbsp;   'engine\_capacity': \[2000],

&nbsp;   'horse\_power': \[190],

&nbsp;   # ... add other required features ...

})



\# 4. Generate Prediction

predicted\_price = predictor.predict(new\_data)



print(f"Estimated Value: {predicted\_price.iloc\[0]:,.0f} PLN")

Performance Summary (Sample)SegmentPrice RangeMAE (Error)MAPE (%)VerdictBudget< 30k PLN~3,300 PLN~25%Volatile (Condition matters more than specs)Economy30k-70k PLN~5,100 PLN~10.7%ReliableMid-Range70k-150k PLN~8,600 PLN~8.3%Highly AccuratePremium150k-300k PLN~16,200 PLN~7.9%ExcellentLuxury> 300k PLN~51,000 PLN~9.1%Strong Trend CaptureNote: Metrics derived from the Holdout set (20% of data).

