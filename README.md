# County-Level Life Expectancy Prediction in the United States

A machine learning project predicting county-level life expectancy (2012-2019) using socioeconomic, atmospheric, and livestock features with XGBoost regression models optimized through Bayesian hyperparameter tuning.

## Project Overview

This project develops predictive models for U.S. county-level life expectancy by integrating multi-source data and applying advanced feature selection techniques. Through systematic feature reduction from 100+ to 40 variables and ablation studies across four model configurations, we achieve strong predictive accuracy (R² = 0.844) while maintaining interpretability. County-level cross-validation (GroupKFold) ensures the model generalizes to geographically unseen counties.

**Key Findings:**
- Top 20 features achieve R² = 0.844 with RMSE = 1.00 years on held-out counties
- Formaldehyde exposure ranked 3rd overall, revealing important environmental health implications
- Wet-bulb temperature ranked 5th, indicating heat stress as a health determinant
- 50% feature reduction achieved with no performance loss

## Dataset

**Temporal Scope:** 2012-2019
**Geographic Coverage:** ~3,100 U.S. counties
**Total Observations:** 24,487 county-year pairs
**Final Features:** 40 (after systematic reduction)

### Data Sources

| Category | Source | Variables |
|----------|--------|-----------|
| **Socioeconomic** | U.S. Census Bureau (ACS 5-Year) | Poverty rate, education, disability rate, etc. (10 features) |
| **Atmospheric** | CAMS/ERA5 | Pollutants, temperature, humidity, aerosols (23 features) |
| **Livestock** | FAO GLW | Cattle, poultry, hogs, sheep, horses, etc. (7 features) |
| **Target** | IHME | County-level life expectancy at birth |

## Quick Start

### Prerequisites
```bash
Python 3.9+
pandas, numpy, scikit-learn, xgboost, scikit-optimize, shap, matplotlib, seaborn
```

### Installation
```bash
git clone https://github.com/samyakshrestha/predicting-life-expectancy.git
cd predicting-life-expectancy
pip install -r requirements.txt
```

### Run the Pipeline
```bash
# Execute notebooks in sequence (02 through 09)
jupyter notebook notebooks_clean/
```

## Project Structure

```
├── data_cleaned/                  # All processed datasets and outputs
│   ├── raw/                      # Raw source data
│   ├── demographics_final/       # Processed demographic data
│   ├── weather/                  # Weather variables
│   ├── livestock/                # Livestock inventory data
│   ├── processed/                # Intermediate processed datasets
│   ├── combined_final/           # Final reduced dataset (40 features)
│   └── outputs_cleaned/          # Model outputs and figures
├── notebooks_clean/               # Analysis pipeline (02-09)
│   ├── 02_fetch_merge_acs_variables.ipynb
│   ├── 03_combine_features_by_year.ipynb
│   ├── 04_cleaning_dataset.ipynb
│   ├── 05_combine_all_datasets.ipynb
│   ├── 06_feature_analysis_demographics.ipynb
│   ├── 07_feature_analysis_weather.ipynb
│   ├── 08_create_final_reduced_dataset.ipynb
│   └── 09_xgboost_bayesian_optimization.ipynb
└── docs/
    └── PROJECT_METHODOLOGY.md     # Comprehensive methodology
```

## Methodology

### 1. Data Integration (Notebooks 02-05)
- Fetch ACS demographic variables via API
- Merge demographics, weather, and livestock data by FIPS code
- Clean and validate combined dataset

### 2. Feature Selection (Notebooks 06-08)
- **Correlation Analysis:** Identify highly correlated features (|r| > 0.85)
- **Hierarchical Clustering:** Remove redundant atmospheric variables
- **Domain Filtering:** Exclude irrelevant variables
- **Result:** Reduced from ~100 features to 40 final predictors

### 3. Modeling (Notebook 09)
- **Algorithm:** XGBoost Regressor
- **Optimization:** Bayesian hyperparameter search (30 iterations, 5-fold GroupKFold CV)
- **Cross-Validation:** County-level grouping (GroupShuffleSplit for train/test, GroupKFold for CV) to prevent data leakage
- **Configurations:** All Features (40), Top 20, Top 10, Top 5
- **Evaluation:** RMSE, R², MAE, permutation importance, SHAP analysis

## Results

### Model Performance Comparison

| Model | Features | Train R² | Test R² | Train RMSE | Test RMSE | Test MAE |
|-------|----------|----------|---------|------------|-----------|----------|
| **All Features** | 40 | 0.939 | 0.844 | 0.63 | 1.00 | 0.76 |
| **Top 20** | 20 | 0.985 | 0.844 | 0.31 | 1.00 | 0.76 |
| **Top 10** | 10 | 0.922 | 0.803 | 0.71 | 1.13 | 0.87 |
| **Top 5** | 5 | 0.851 | 0.756 | 0.98 | 1.25 | 0.95 |

**Recommended model:** Top 20 features - achieves equivalent test performance (R² = 0.844) to the full model with 50% fewer features. Test metrics reflect county-level cross-validation, where the model predicts life expectancy for counties not seen during training.

### Key Finding: Formaldehyde and Wet-Bulb Temperature as Top Predictors

**Formaldehyde exposure** ranked 3rd overall in SHAP importance and 2nd in permutation importance, surpassing several traditional socioeconomic indicators. This finding suggests that air quality plays a more significant role in population health than traditionally recognized. **Wet-bulb temperature**, a physiological measure of heat stress, ranked 5th overall, indicating that climate-related factors capture health-relevant information beyond standard temperature measurements.

### Visualizations

The project generates publication-ready figures including:
- Prediction scatter plots with performance metrics
- Residual analysis plots
- Permutation importance rankings
- SHAP summary (beeswarm) and dependence plots
- Ablation study showing performance vs. feature count trade-offs

*All outputs saved to: `data_cleaned/outputs_cleaned/modeling/xgboost/`*

## Technologies

- **Python 3.9+**
- **XGBoost** - Gradient boosting framework
- **scikit-optimize** - Bayesian optimization
- **SHAP** - Model interpretability
- **pandas & numpy** - Data manipulation
- **matplotlib & seaborn** - Visualization

### Data Sources
- **Life Expectancy:** Institute for Health Metrics and Evaluation (IHME)
- **Socioeconomic:** U.S. Census Bureau, American Community Survey (ACS 5-Year)
- **Atmospheric:** Copernicus Atmosphere Monitoring Service (CAMS), ERA5 Reanalysis
- **Livestock:** FAO Gridded Livestock of the World (GLW)

## Documentation

For detailed methodology, see [PROJECT_METHODOLOGY.md](docs/PROJECT_METHODOLOGY.md)

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Author

**Samyak Shrestha**  

---

*Last Updated: January 2026*
