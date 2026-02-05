"""
Generate a publication-quality choropleth map showing US county-level
life expectancy for 2019, for the paper's Introduction section.
"""

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# LOAD DATA
# ============================================================
# Load shapefile
shapefile_path = '/Users/samyakshrestha/Projects/Life Expectancy Project/data/shapefiles/cb_2019_us_county_20m.shp'
counties = gpd.read_file(shapefile_path)

# Load life expectancy data
data_path = '/Users/samyakshrestha/Projects/Life Expectancy Project/data_cleaned/combined_final/final_combined_all_variables_reduced.csv'
le_data = pd.read_csv(data_path)

# Filter to 2019
le_2019 = le_data[le_data['Year'] == 2019].copy()

# Prepare FIPS codes for merging
le_2019['GEOID'] = le_2019['Fips'].astype(str).str.zfill(5)
counties['GEOID'] = counties['GEOID'].astype(str).str.zfill(5)

# Merge with shapefile
counties = counties.merge(le_2019[['GEOID', 'Mean Life Expectancy']], on='GEOID', how='left')

# Filter to continental US (exclude Alaska, Hawaii, Puerto Rico, etc.)
exclude_states = ['02', '15', '60', '66', '69', '72', '78']
counties = counties[~counties['STATEFP'].isin(exclude_states)]

# ============================================================
# CREATE FIGURE
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(12, 7))

# Plot choropleth
counties.plot(
    column='Mean Life Expectancy',
    ax=ax,
    cmap='RdYlGn',
    legend=True,
    legend_kwds={
        'label': 'Life Expectancy (years)',
        'orientation': 'vertical',
        'shrink': 0.7,
        'pad': 0.02,
        'aspect': 20
    },
    missing_kwds={'color': '#e0e0e0', 'label': 'No data'},
    edgecolor='white',
    linewidth=0.1
)

# Add title
ax.set_title('County-Level Life Expectancy in the United States (2019)',
             fontsize=14, fontweight='bold', pad=10)

# Clean up axes
ax.axis('off')
ax.set_aspect('equal')

# Add data source note (bottom left, out of the way)
le_min = counties['Mean Life Expectancy'].min()
le_max = counties['Mean Life Expectancy'].max()
ax.text(0.01, 0.02, f'n = {len(le_2019):,} counties',
        transform=ax.transAxes, ha='left', va='bottom', fontsize=9, color='#666666')

plt.tight_layout()

# ============================================================
# SAVE
# ============================================================
output_dir = '/Users/samyakshrestha/Projects/Life Expectancy Project/paper/Figures'
plt.savefig(f'{output_dir}/fig1_life_expectancy_map_2019.png',
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.savefig(f'{output_dir}/fig1_life_expectancy_map_2019.pdf',
            bbox_inches='tight', facecolor='white', edgecolor='none')

print(f"Choropleth map saved to {output_dir}/fig1_life_expectancy_map_2019.png and .pdf")
print(f"Life expectancy range: {le_min:.1f} - {le_max:.1f} years")
print(f"Counties with data: {counties['Mean Life Expectancy'].notna().sum()}")
