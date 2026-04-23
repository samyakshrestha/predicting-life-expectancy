# Life Expectancy Project — Full Context

## Overview

This project predicts county-level life expectancy across the United States using an integrated
dataset of atmospheric, socioeconomic, and livestock variables, modeled with XGBoost and
interpreted using SHAP. It is the first paper in a series of county-level health outcome
prediction studies from the same lab.

**Paper title:** "The External Exposome and Life Expectancy: Formaldehyde as a Leading
Predictor in U.S. Counties"

**Target journal:** MDPI Air (submitted; invited submission with full APC waiver from
Dr. Ting Leng, Managing Editor)

**Status:** Submitted. Major revision received.

---

## Research Program Context

This is paper 1 of an ongoing series using the same XGBoost + SHAP + Bayesian optimization
pipeline across different health outcomes:

1. **Life expectancy** (this repo) — submitted to MDPI Air
2. **CVD mortality** — submitted to MDPI AI Sensors
3. **CRD mortality** — pipeline complete, paper in progress
4. **Lung cancer mortality** — pipeline complete, paper in progress

All papers share the same 43-feature integrated dataset (atmospheric + socioeconomic +
livestock) and the same modeling pipeline. The LE paper is the structural blueprint.

**EB2 context:** The author (Samyak Shrestha) is building a research program for an EB2
National Interest Waiver application. Publication count matters.

---

## Authors

- Samyak Shrestha (samyak.shrestha@utdallas.edu)
- David J. Lary (david.lary@utdallas.edu) — corresponding author
- Shisir Ruwali (shisir.ruwali@utdallas.edu)
- Faiz Ahmad (faiz.ahmad@utdallas.edu)

**Affiliation:** Department of Physics, The University of Texas at Dallas, Richardson, TX 75080

---

## Dataset

**Spatial coverage:** All counties in the contiguous United States
**Temporal coverage:** 2012–2019
**Final dataset:** 24,487 county-year observations, 43 predictor variables, 1 target variable
**Target:** Life expectancy at birth (years), total population, IHME county estimates

### Data Sources

| Source | Description | Resolution | N features |
|--------|-------------|------------|------------|
| IHME | Life expectancy at birth (all races, under 1 yr age group) | County-level | 1 (target) |
| ACS 5-year | Socioeconomic and demographic indicators | County-level | 10 |
| CAMS/ERA5 | Atmospheric pollutants and meteorological variables | County-level (from 0.75°/0.25° grids) | 26 |
| FAO GLW | Livestock density by species | County-level (from ~10 km grid) | 7 |
| **Total** | | | **43 features** |

### ACS Variables (10)

Poverty rate, median household income, unemployment rate, educational attainment (bachelor's
degree or higher %), racial composition (White, Black, Hispanic, Asian %), single mother
families %, households with no vehicle %, disability rate, total population.

### CAMS/ERA5 Variables (26)

Atmospheric pollutants (PM2.5, O3, NO2, formaldehyde, sulphate, black carbon, dust, propane,
nitric acid), meteorological variables (wet-bulb temperature, 10m wind speed, leaf area indices
for high and low vegetation, relative humidity). Several variables expressed as FoT (fraction
of time) metrics: proportion of the year when concentrations exceeded the 75th percentile
across all observations. CAMS EAC4 at 0.75°×0.75°, 3-hourly resolution. ERA5 at 0.25°×0.25°.
CAMS assimilates satellite observations: OMI (tropospheric composition), MODIS (aerosol optical
depth), GOME-2 (trace gases).

### FAO GLW Variables (7)

Livestock density (heads/km²): cattle, chicken, duck, goat, horse, pig, sheep. Aggregated to
county boundaries using area-weighted zonal statistics. GLW discrete years (2010, 2015, 2020)
linearly interpolated for 2012–2019.

---

## Data Processing

- Merged by county FIPS code and year
- Missing values (-666666666 sentinel or NaN) handled via listwise deletion
- Features with pairwise correlation > 0.85 removed via hierarchical clustering (most
  interpretable feature from each correlated cluster retained)
- Metadata columns (County, State, FIPS) excluded from feature matrix

---

## Train-Test Split

**Method:** GroupShuffleSplit with county FIPS as grouping variable

This is non-negotiable. Because observations are stacked across 8 years, standard random
splitting would allow the same county to appear in both train and test sets — data leakage.
GroupShuffleSplit ensures every observation from a given county is in either train or test,
never both.

- **Training set:** 19,583 observations (2,448 counties, 80%)
- **Test set:** 4,904 observations (613 counties, 20%)

The test score represents "future unseen county" performance — the model must generalize to
entirely new geographic regions.

---

## Modeling Pipeline

**Notebooks** (in `notebooks_clean/`):

| Notebook | Purpose |
|----------|---------|
| `00_single_year_life_expectancy.ipynb` | Extract IHME LE data |
| `01_preprocessing_fips_life_expectancy.ipynb` | FIPS cleaning and standardization |
| `02_fetch_merge_acs_variables.ipynb` | ACS data via Census API |
| `03_combine_features_by_year.ipynb` | Combine CAMS/ERA5 atmospheric features by year |
| `04_cleaning_dataset.ipynb` | Clean and standardize |
| `05_combine_all_datasets.ipynb` | Merge all four data sources |
| `06_feature_analysis_demographics.ipynb` | Correlation analysis, ACS features |
| `07_feature_analysis_weather.ipynb` | Correlation analysis, atmospheric features |
| `08_create_final_reduced_dataset.ipynb` | Final feature selection and dataset creation |
| `09_xgboost_bayesian_optimization_run1.ipynb` | Main modeling (source of results) |
| `10–11_xgboost_bayesian_optimization_run*.ipynb` | Additional runs / ablation variants |

**Final dataset:** `data_cleaned/combined_final/final_combined_all_variables_reduced.csv`

---

## Modeling Approach

**Algorithm:** XGBoost gradient boosting regressor

**Hyperparameter optimization:** BayesSearchCV (scikit-optimize) with 30 iterations and
5-fold GroupKFold cross-validation (R² as optimization metric). GroupKFold prevents county
leakage during CV.

**Optimal hyperparameters (all-features model):**

| Parameter | Value |
|-----------|-------|
| n_estimators | 1457 |
| max_depth | 7 |
| learning_rate | 0.024 |
| subsample | 0.95 |
| colsample_bytree | 0.50 |
| reg_alpha | 0.08 |
| reg_lambda | 5.00 |
| min_child_weight | 15 |

**Interpretability:**
- SHAP values via TreeExplainer: quantifies each feature's contribution to individual
  predictions; accounts for feature interactions
- Permutation importance: randomly shuffles each feature and measures RMSE degradation
- Ablation study: retrains with top 20, top 10, top 5 features (hyperparameters
  reoptimized for each subset)

---

## Results

### Model Performance

| Model | Train R² | Test R² | Train RMSE | Test RMSE | Test MAE |
|-------|----------|---------|------------|-----------|---------|
| All 43 features | 0.989 | 0.854 | 0.26 yr | 0.97 yr | ~0.74 yr |
| Top 20 | — | 0.834 | — | 1.03 yr | — |
| Top 10 | — | 0.797 | — | 1.14 yr | — |
| Top 5 | — | 0.754 | — | 1.26 yr | — |

The train-test gap is expected and by design (GroupShuffleSplit). Test R² > 0.85 with an
average error under one year per county is the headline result.

### SHAP Feature Importance — Top 20 (All-Features Model)

| Rank | Feature |
|------|---------|
| 1 | Bachelor's Degree or Higher (%) |
| 2 | FoT Formaldehyde Above 75th Percentile |
| 3 | Poverty Rate |
| 4 | Disability Rate |
| 5 | Wet-Bulb Temperature |
| 6 | Single Mother Families (%) |
| 7 | Hispanic Population (%) |
| 8 | White Population (%) |
| 9 | Leaf Area Index, High Vegetation |
| 10 | Total Population |
| 11 | FoT Propane Above 75th Percentile |
| 12 | Households with No Vehicle (%) |
| 13 | Horse |
| 14 | Hydrophilic Black Carbon Aerosol Mixing Ratio |
| 15 | Leaf Area Index, Low Vegetation |
| 16 | Pig |
| 17 | FoT Nitric Acid Above 75th Percentile |
| 18 | Dust Aerosol (0.9–20 µm) Mixing Ratio |
| 19 | Chicken |
| 20 | Cattle |

**Key finding:** Formaldehyde (FoT above 75th percentile) ranks 2nd among all 43 predictors,
ahead of poverty rate and all other socioeconomic variables except educational attainment.
Wet-bulb temperature ranks 5th. Atmospheric variables account for 2 of the top 5 predictors.

### Permutation Importance (Top 20 Model)

Rank order: Educational attainment (1st), Disability rate (2nd), Formaldehyde (3rd),
Poverty rate (4th). The reordering of formaldehyde vs. disability between SHAP and permutation
importance is discussed in the paper — both methods independently confirm formaldehyde in
top 3.

---

## Figures Used in the Paper

**In `paper/Figures/`:**
- `fig1_life_expectancy_map_2019_quintile.png` — opening choropleth, 2019 IHME data,
  quintile-based bins, values range 67.6–92.3 years
- `fig1_scatter_performance_all_features.png` — predicted vs. actual scatter, train and test
- `fig7b_residual_analysis_top20.png` — 3-panel residual diagnostics (residuals vs. fitted,
  residuals vs. poverty rate, residual histogram)
- `fig4_shap_summary_all_features.png` — SHAP beeswarm, top 20 predictors
- `fig10_permutation_importance_top20.png` — permutation importance bar chart, top 20 model
- `fig28_ablation_study.png` — ablation curve (Test R² and RMSE vs. number of features)
- `graphic_abstract.png` — study workflow diagram

**Never use:**
- fig2, fig9, fig16, fig22 — mislabeled as Q-Q plots; actually predicted-vs-true agreement
  plots. Redundant with scatter and incorrectly titled. Excluded from paper.

---

## Key Scientific Framing

**External exposome framework (Wild 2012):** The paper explicitly frames the analysis within
the external exposome — the totality of environmental exposures encountered throughout a
lifetime. This distinguishes the paper from standard socioeconomic determinants studies.

**Formaldehyde as a predictor:** FoT Formaldehyde Above 75th Percentile ranks 2nd overall.
Biological mechanisms in the literature: leukemia and Hodgkin's disease (BeaneFreeman2009).
Ground-based monitoring is sparse; satellite monitoring (OMI/TROPOMI) fills the gap.
The FoT metric captures exposure frequency, not just magnitude.

**Wet-bulb temperature:** A physiological measure of heat stress (not just air temperature).
35°C wet-bulb is the theoretical survivability limit (Sherwood and Huber 2010). Ranking
5th makes it the second atmospheric variable in the top 5.

**Livestock as proxies:** Livestock density proxies for localized air quality degradation
(NH3, CH4, N2O emissions) and zoonotic disease risk.

---

## File Paths

| File | Purpose |
|------|---------|
| `paper/template.tex` | Submitted manuscript (MDPI Air, `air` class) |
| `paper/references.bib` | Citation library |
| `paper/CONTEXT.md` | Earlier context document (less complete than this file) |
| `notebooks_clean/09_xgboost_bayesian_optimization_run1.ipynb` | Source of all results |
| `data_cleaned/combined_final/final_combined_all_variables_reduced.csv` | Final dataset |
| `data_cleaned/outputs_cleaned/modeling/xgboost/table*.csv` | Metrics CSVs |
| `data_cleaned/outputs_cleaned/modeling/xgboost/fig*.png` | All generated figures |

---

## Citations Already in references.bib

- `\cite{IHME_county_LE_2000_2019}` — IHME LE dataset
- `\cite{uscensus_acs5year_2024}` — ACS 5-year estimates
- `\cite{Inness2019}` — CAMS EAC4 + satellite instruments
- `\cite{chen2016xgboost}` — XGBoost
- `\cite{LundbergLee2017}` — SHAP
- `\cite{skopt_bayessearchcv}` — BayesSearchCV
- `\cite{Gilbert2018}` — FAO livestock
- `\cite{Wild2012}` — External exposome framework
- `\cite{Chetty2016_IncomeLifeExpectancy}` — Income and health
- `\cite{SinghLee2021}` — Socioeconomic determinants
- `\cite{BeaneFreeman2009_FormaldehydeMortality}` — Formaldehyde and leukemia/Hodgkin's
- `\cite{Raymond2020EmergenceHeatHumidity}` — Wet-bulb temperature
- `\cite{Sherwood2010AdaptabilityLimit}` — 35°C wet-bulb limit
- `\cite{Mora2017GlobalDeadlyHeat}` — Heat mortality
- `\cite{Pampel2010SocioeconomicHealthBehaviors}` — Omitted variable bias (SES ~ smoking)
- `\cite{DeSmedt2021TROPOMIOMI}` — TROPOMI/OMI formaldehyde monitoring
- `\cite{salthammer2019formaldehyde}` — Formaldehyde sources

---

## Writing Preferences

- No em dashes. Use commas, colons, or restructure sentences.
- Write entire sections at a time. User reviews and approves before moving on.
- Verify every number from source CSV files before writing it in the paper.
- Do not add comments or docstrings to code unless the logic is non-obvious.
- Keep responses concise and direct.
