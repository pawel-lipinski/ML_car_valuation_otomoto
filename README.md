# Otomoto Car Price Prediction Model (train data - DEC 2025)

## Project Overview

This project is an end-to-end Machine Learning pipeline designed to predict used car prices in the Polish market (Otomoto).

Unlike simple regression models, this system uses **AutoGluon's "Best Quality" Multi-Layer Stacking**, which ensembles Neural Networks, CatBoost, and LightGBM models to achieve state-of-the-art accuracy. It is specifically engineered to handle the complexities of the Polish market, including regional price differences, budget car anomalies, and luxury vehicle valuations.


## Key Features



### Model Architecture

* **AutoGluon Stacking:** Utilizes a multi-layer ensemble strategy (Stacking \& Bagging) rather than a single algorithm.

* **Auto-Tuning:** Automatically optimizes hyperparameters for maximum MAE (Mean Absolute Error) reduction.

### Feature Engineering

* **Automated Translation:** Translates categorical features (Color, Body Type, Transmission) from Polish to English using `deep\_translator`.

* **Geo-Spatial Intelligence:** Calculates `dist\_to\_warsaw` (distance to capital) to account for regional purchasing power differences.

* **Power-to-Weight Parsing:** Extracts numeric data from messy string fields (e.g., "150 KM", "2000 cm3").

### Robustness \& Safety

* **"Shielded" Outlier Detection:** A custom Isolation Forest implementation that removes statistical anomalies (e.g., a 10M PLN Volkswagen Golf) while "shielding" legitimate luxury cars (Ferrari, Lamborghini, AMG) from being deleted.


 

## Project Structure




├── data/

│    ├── raw\_data.csv                  Raw scraping data (Input)

│    ├── train.csv                      Cleaned training dataset

│    └── test.csv                       Holdout dataset (20%)

│

├── saved\_models/                     PRODUCTION ARTIFACTS (DEPLOY FROM HERE)

│    ├── autogluon\_pro\_ensemble/     The Champion Model (Contains model artifacts)

│    └── feature\_columns.pkl          Critical: List of column names/order required for prediction

│

├── ag\_models\_benchmark/             Temporary: Output from initial "Quick Shootout"

├── ag\_models\_pro/                   Temporary: Working directory for heavy training

│

└── otomoto\_model\_training\_2026.ipynb Main Training \& Audit Pipeline





**Pipeline Workflow.**
1. **Data Ingestion \& Cleaning.** The notebook otomoto\_model\_training\_2026.ipynb loads raw data, parses numeric values, and handles missing data. It applies a Shielded Isolation Forest to remove corrupted records without losing high-value inventory.
2. **Training (AutoGluon Pro).** We use the presets='best\_quality' configuration. This trains models in layers:
Layer 1: CatBoost, XGBoost, Neural Net Torch, LightGBM.
Layer 2: A meta-learner that combines the outputs of Layer 1 to correct their biases.
3. **Professional Audit.** The pipeline includes a comprehensive auditing suite:
- Segmented Performance Matrix: Evaluates MAE/MAPE across Budget, Economy, Mid-Range, Premium, and Luxury tiers. Residual Analysis: Visualizes heteroscedasticity.
- Brand Bias Scorecard: Identifies if the model systematically overprices or underprices specific brands (e.g., Dacia vs. Porsche).
- The "Black Book": Automatically flags the top worst over-valuations and under-valuations for manual review.

**Installation \& Requirements**
Ensure you have the necessary Python libraries installed:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost catboost shap deep-translator joblib autogluon
```
Note: CUDA (GPU) is recommended for training but not required for inference.


**Performance Summary (Sample) - AutoGluon model**
| Segment | Price Range | MAE (Error) | MAPE (%) | Verdict |
|---------|--------------|-------------|----------|---------|
| Budget | < 20k PLN | ~3,150 PLN | ~31.8% | Volatile (Condition matters more than specs) |
| Economy | 20k-50k PLN | ~4,200 PLN | ~12.4% |Reliable |
| Mid-Range | 50k-100k PLN | ~6,600 PLN | ~9.1% | Highly Accurate |
| Premium | 100k-250k PLN | ~12,200 PLN | ~8.0 | Excellent |
| Luxury | > 250k PLN | ~37,500 PLN | ~8.9% | Strong Trend Capture |

Note: Metrics derived from the Holdout set (20% of data).

