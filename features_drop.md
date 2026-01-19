# Feature Selection Methodology: Handling Multicollinearity in Atmospheric Variables

## 1. Exclusion Criteria
To ensure model stability and interpretability, we applied a systematic **"Survivor Protocol"** to reduce multicollinearity among the high-dimensional atmospheric feature set. Variables were flagged for potential exclusion if they met either of the following thresholds:
* **Pearson Correlation Coefficient ($r$) > 0.90** with another feature.
* **Variance Inflation Factor (VIF) > 100**.

For identified pairs/clusters of collinear variables, we retained a single representative feature based on the following hierarchy of decision rules:
1.  **Interpretability:** Physical measurements (e.g., Temperature) were preferred over statistical derivatives (e.g., Fraction of Time > 75th percentile).
2.  **Robustness:** Aggregate satellite measures (e.g., AOD) were preferred over component mixing ratios unless specific chemical composition was the target of study.
3.  **Predictive Power:** In tie-breaking scenarios, the variable with the stronger independent correlation to the target (Life Expectancy) was retained.

## 2. Variable Exclusion Log

### A. The "Heat Stress" Cluster
* **Retained:** `Wet Bulb Temperature`
* **Dropped:** `FoT Temperature > 75th percentile`, `FoT Temperature < 25th percentile`, `FoT Hydrogen Peroxide`.
* **Justification:** The variables in this cluster exhibited extreme collinearity ($r > 0.93$). `Wet Bulb Temperature` was selected as the survivor because it is the standard physiological metric for heat stress, capturing the combined lethality of heat and humidity. The "Fraction of Time" (FoT) variables provided redundant signal but with higher sensitivity to arbitrary threshold definitions.

### B. The "Summer Photochemistry" Cluster
* **Retained:** `FoT Formaldehyde > 75th percentile`
* **Dropped:** `Isoprene`, `FoT Isoprene`, `FoT Peroxyacetyl Nitrate`, `FoT Ozone`.
* **Justification:** Isoprene and Formaldehyde are chemically linked precursors to ozone formation, resulting in a correlation of $r > 0.93$. `Formaldehyde` was retained because it demonstrated the highest independent correlation with mortality in our dataset ($r = -0.56$), serving as the strongest proxy for the "summer smog" regime.

### C. The "Aerosol & Combustion" Cluster
* **Retained:** `Sulphate AOD` (Industrial/Coal Proxy) and `Sea Salt AOD`.
* **Dropped:** `Carbon Monoxide`, `Ethane`, `Hydrophilic/Hydrophobic Black Carbon`, `Organic Matter Mixing Ratios`, `Sea Salt Mixing Ratios`.
* **Justification:** High multicollinearity ($r > 0.88$) exists between various combustion byproducts. `Sulphate AOD` was retained as the primary proxy for anthropogenic industrial pollution due to its high predictive signal ($r = -0.43$). The specific chemical breakdowns (e.g., Hydrophilic vs. Hydrophobic) added model complexity (VIF > 1000) without providing distinct mortality signals distinguishable from the aggregate AOD measures.

### D. The "Atmospheric Pressure" Cluster
* **Retained:** `Mean Sea Level Pressure`
* **Dropped:** `Surface Pressure`
* **Justification:** These two variables are physically redundant ($r \approx 1.0$) for the purpose of mortality modeling. Mean Sea Level Pressure was retained as the standard meteorological convention.

# Feature Selection Justification: Exclusion of Collinear Atmospheric Variables

## 1. Exclusion of Photochemical Precursors and Secondary Oxidants
**Variables Excluded:** `FoT Isoprene > 75th Percentile`, `FoT Peroxyacetyl Nitrate (PAN) > 75th Percentile`
**Variable Retained:** `FoT Formaldehyde > 75th Percentile`

### A. Statistical Justification
Our preliminary multicollinearity analysis identified a tight cluster of covariance among photochemical oxidants. Specifically, `FoT Isoprene` and `FoT PAN` exhibited extreme Pearson correlation coefficients with `FoT Formaldehyde` ($r = 0.935$ and $r = 0.919$, respectively).

Inclusion of all three variables would introduce significant variance inflation, destabilizing the model's feature importance rankings without adding unique information. To resolve this, we employed a "Champion Selection" strategy based on predictive power. `FoT Formaldehyde` demonstrated the strongest independent correlation with the target variable (Life Expectancy) at $r = -0.56$, compared to Isoprene ($r = -0.53$) and PAN ($r = -0.49$).

### B. Physical & Chemical Justification
The statistical covariance observed is grounded in atmospheric chemistry.
* **Isoprene** is a volatile organic compound (VOC) emitted by vegetation during high-temperature stress. It acts as a primary precursor in the formation of tropospheric ozone and secondary organic aerosols.
* **Formaldehyde (HCHO)** is an intermediate oxidation product rapidly formed when Isoprene reacts with hydroxyl radicals ($OH$) in the presence of sunlight.
* **PAN** is a secondary pollutant formed through the reaction of peroxyacetyl radicals (from VOC oxidation) with nitrogen dioxide ($NO_2$).

Because these species are physically linked in the same rapid photochemical reaction chain (driven by heat and sunlight), they appear as a singular "Summer Smog" signal in long-term observational data. Retaining `FoT Formaldehyde` serves as the most robust proxy for this entire photochemical regime, capturing both the biogenic source (covariance with Isoprene) and the oxidative stress capacity of the atmosphere.

## 2. Exclusion of Snow Albedo
**Variables Excluded:** `Snow Albedo`
**Variable Retained:** `Snow Depth`

### A. Statistical Justification
While `Snow Albedo` showed only moderate pairwise correlation with `Snow Depth`, it exhibited an extremely high Variance Inflation Factor (VIF > 8,000). This indicates that `Snow Albedo` is a linear combination of other variables in the dataset (specifically `Snow Depth`, `Temperature`, and `Vegetation Index`).

### B. Physical Justification
Albedo is a radiative property dependent on the presence of snow.
* If `Snow Depth > 0`, Albedo is high.
* If `Snow Depth = 0`, Albedo is determined by the underlying land cover (captured by `Leaf Area Index` and `Land-Sea Mask`).

Therefore, `Snow Albedo` provides no unique environmental information regarding mortality risks (such as cold stress or isolation) that is not already captured by `Snow Depth`. Its exclusion reduces model complexity by removing a mathematically redundant dependent variable.

## 3. Resulting Feature Set
This reduction process condensed the atmospheric variable set from 45 raw features to **13 distinct environmental drivers**, effectively minimizing the risk of VIF-induced coefficient instability while preserving the core signals for Heat, Photochemical Smog, Industrial Pollution, and Particulate Matter.



# Feature Selection Methodology: Socioeconomic & Demographic Variables (ACS)

## 1. Final Feature Set
The following 9 variables were selected as the core socioeconomic inputs for the mortality prediction model. These features were chosen to maximize predictive signal while minimizing multicollinearity (VIF < 10 for all selected features).

* **Poverty Rate:** The primary proxy for economic deprivation and material hardship.
* **Bachelor's Degree %:** A proxy for health literacy, elite socioeconomic status, and occupational safety.
* **Disability Rate:** A direct measure of the population's existing health burden.
* **Unemployment Rate:** A measure of acute economic instability and labor market stress.
* **Single Mother Families %:** A proxy for household structural vulnerability and social support constraints.
* **Black Population %:** Captures systemic disparities and social determinants of health specific to racial inequality.
* **Hispanic Population %:** Included to capture the "Hispanic Paradox" (statistically higher life expectancy despite lower socioeconomic status).
* **Households w/ No Vehicle %:** A proxy for physical isolation and lack of access to healthcare/resources.
* **Total Population:** Control variable for county size and density.

## 2. Exclusion Criteria & Decision Log

Variables were excluded based on a combination of **High Variance Inflation Factor (VIF > 10)** indicating redundancy, or **Negligible Correlation ($|r| < 0.05$)** with the target variable.

### A. Dropped: Rent Burden (+50% of Income)
* **Metrics:** Correlation with Target = `0.019`; VIF = `15.2`.
* **Rationale:** Despite its theoretical importance, Rent Burden showed zero linear relationship with Life Expectancy in this dataset. This is likely due to the "Cost of Living Confounder," where high rent burdens are found in both impoverished areas (low life expectancy) and wealthy, high-amenity metropolitan areas (high life expectancy). The signal canceled itself out.

### B. Dropped: Median Household Income & Gini Index
* **Metrics:** Income VIF = `53.2`; Gini VIF = `272.1`.
* **Rationale:** Both variables exhibited extreme multicollinearity with `Poverty Rate`. The model could not mathematically distinguish between "Low Income," "High Inequality," and "High Poverty."
* **Decision:** `Poverty Rate` was retained as the superior predictor because it specifically measures deprivation (lack of basic needs), which is a stronger biological driver of mortality than median income or inequality coefficients.

### C. Dropped: White Population %
* **Metrics:** VIF = `115.4`.
* **Rationale:** This variable was mathematically redundant because it is a linear combination of the other racial categories ($White \approx 100 - (Black + Hispanic)$). Including it introduced massive instability. It was dropped to allow the `Black` and `Hispanic` coefficients to resolve clearly.

### D. Dropped: High School Degree %
* **Metrics:** VIF = `278.7`.
* **Rationale:** This variable acted as the inverse "mirror image" of `Bachelor's Degree %`. Including both the floor (High School) and the ceiling (Bachelor's) created a singularity in the education signal. `Bachelor's Degree %` was retained as it had a stronger correlation with the target ($r=0.64$ vs $r=0.55$).

### E. Dropped: Median Age
* **Metrics:** VIF = `129.4`.
* **Rationale:** Excluded due to **Endogeneity**. Using Median Age to predict Life Expectancy introduces data leakage (populations with high life expectancy naturally become older). Additionally, it confounded the `Disability Rate` signal.