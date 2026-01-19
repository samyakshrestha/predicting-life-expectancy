# County-Level Life Expectancy Prediction in the United States

A comprehensive machine learning project predicting county-level life expectancy (2012-2019) using demographic, weather, and livestock features with XGBoost regression models optimized through Bayesian hyperparameter tuning.

## Project Overview

This project develops predictive models for U.S. county-level life expectancy by integrating multi-source data and applying advanced feature selection techniques. Through systematic feature reduction from 126 to 42 variables and ablation studies across four model configurations, we achieve high predictive accuracy (R² ≈ 0.95-0.97) while maintaining interpretability.

**Key Findings:**
- Top 20 features achieve exceptional performance with R² = 0.97
- Formaldehyde emerged as a top predictor, revealing important environmental health implications
- 67% feature reduction achieved with minimal performance loss
- Environmental factors play a more significant role than previously recognized

## Dataset

**Temporal Scope:** 2012-2019  
**Geographic Coverage:** ~3,000 U.S. counties  
**Total Observations:** ~24,000 county-year pairs  
**Final Features:** 42 (after systematic reduction)

### Data Sources

| Category | Source | Variables |
|----------|--------|-----------|
| **Demographics** | U.S. Census Bureau (ACS 5-Year) | Poverty rate, education, population density, etc. (9 features) |
| **Weather** | CAMS ECMWF | Temperature, precipitation, humidity, solar radiation (~21 features) |
| **Livestock** | FAO GLM | Cattle, poultry, hogs, sheep inventory (8 features) |
| **Target** | IHME | County-level mean life expectancy |

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
│   ├── combined_final/           # Final reduced dataset (42 features)
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
- **Correlation Analysis:** Identify highly correlated features (|r| > 0.7)
- **VIF Analysis:** Remove multicollinear features (VIF > 10)
- **Domain Filtering:** Exclude irrelevant variables
- **Result:** 88 features removed (6 demographics + 82 weather)

### 3. Modeling (Notebook 09)
- **Algorithm:** XGBoost Regressor
- **Optimization:** Bayesian hyperparameter search (30 iterations, 5-fold CV)
- **Configurations:** All Features (38), Top 20, Top 10, Top 5
- **Evaluation:** RMSE, R², MAE, permutation importance, SHAP analysis

## Results

### Model Performance Comparison

| Model | Features | Train R² | Test R² | Train RMSE | Test RMSE | Train MAE | Test MAE |
|-------|----------|----------|---------|------------|-----------|-----------|----------|
| **All Features** | 41 | 0.999 | 0.962 | 0.090 | 0.489 | 0.068 | 0.360 |
| **Top 20** | 20 | 1.000 | 0.969 | 0.009 | 0.442 | 0.007 | 0.321 |
| **Top 10** | 10 | 0.999 | 0.953 | 0.070 | 0.545 | 0.050 | 0.399 |
| **Top 5** | 5 | 0.948 | 0.801 | 0.577 | 1.121 | 0.438 | 0.851 |

**Recommended model:** Top 20 features - achieves the best test performance (R² = 0.969) with significant dimensionality reduction.

### Key Finding: Formaldehyde as a Top Predictor

A notable discovery from this analysis is that **Formaldehyde concentration** emerged as one of the strongest predictors of life expectancy. This finding has important environmental health implications, suggesting that air quality and indoor/outdoor pollutant exposure may play a more significant role in population health outcomes than traditionally recognized in county-level mortality studies. This result warrants further investigation into the sources and pathways of formaldehyde exposure across U.S. counties and their relationship to public health interventions.

### Visualizations

The project generates 28 publication-ready figures including:
- Prediction scatter plots with performance metrics
- Q-Q plots for distribution validation
- Permutation importance rankings
- SHAP summary and dependence plots
- Correlation heatmaps
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
- **Demographics:** U.S. Census Bureau, American Community Survey

## Documentation

For detailed methodology, see [PROJECT_METHODOLOGY.md](docs/PROJECT_METHODOLOGY.md)

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Author

**Samyak Shrestha**  

---

*Last Updated: January 2026*
