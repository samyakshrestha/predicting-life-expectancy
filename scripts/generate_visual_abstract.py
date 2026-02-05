"""
Generate a visual abstract for the Life Expectancy paper.
Emphasizes formaldehyde as #2 predictor with real US county map.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
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

# Get mean life expectancy per county (across years)
le_by_county = le_data.groupby('Fips')['Mean Life Expectancy'].mean().reset_index()
le_by_county['GEOID'] = le_by_county['Fips'].astype(str).str.zfill(5)

# Merge with shapefile
counties['GEOID'] = counties['GEOID'].astype(str).str.zfill(5)
counties = counties.merge(le_by_county[['GEOID', 'Mean Life Expectancy']], on='GEOID', how='left')

# Filter to continental US (exclude Alaska, Hawaii, Puerto Rico, etc.)
exclude_states = ['02', '15', '60', '66', '69', '72', '78']  # AK, HI, territories
counties = counties[~counties['STATEFP'].isin(exclude_states)]

# ============================================================
# SET UP FIGURE
# ============================================================
fig = plt.figure(figsize=(12, 10))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_facecolor('white')

# Color palette
colors = {
    'title_bg': '#1a365d',
    'highlight': '#c41e3a',
    'bar_normal': '#4a5568',
    'bar_education': '#2d3748',
    'text_light': '#ffffff',
    'text_dark': '#1a202c',
    'text_muted': '#718096',
    'accent': '#3182ce',
    'map_bg': '#f8fafc',
}

# ============================================================
# TITLE SECTION
# ============================================================
title_box = FancyBboxPatch(
    (0.3, 8.5), 11.4, 1.3,
    boxstyle="round,pad=0.02,rounding_size=0.1",
    facecolor=colors['title_bg'],
    edgecolor='none'
)
ax.add_patch(title_box)

ax.text(6.0, 9.35, 'Formaldehyde Exposure:',
        ha='center', va='center', fontsize=22, fontweight='bold',
        color=colors['text_light'])
ax.text(6.0, 8.85, '#2 Predictor of U.S. County Life Expectancy',
        ha='center', va='center', fontsize=17,
        color=colors['text_light'])

# ============================================================
# LEFT SIDE: Real US County Map
# ============================================================
map_box = FancyBboxPatch(
    (0.3, 3.0), 6.4, 5.0,
    boxstyle="round,pad=0.02,rounding_size=0.15",
    facecolor=colors['map_bg'],
    edgecolor='#cbd5e0',
    linewidth=1
)
ax.add_patch(map_box)

ax.text(3.5, 7.7, 'County-Level Life Expectancy', ha='center', va='center',
        fontsize=13, fontweight='bold', color=colors['text_dark'])

# Create inset axes for the map
map_ax = inset_axes(ax, width="95%", height="75%",
                    bbox_to_anchor=(0.35, 3.2, 6.0, 4.3),
                    bbox_transform=ax.transData,
                    loc='center')

# Plot choropleth
counties.plot(
    column='Mean Life Expectancy',
    ax=map_ax,
    cmap='RdYlGn',
    legend=False,
    missing_kwds={'color': '#e2e8f0'},
    edgecolor='white',
    linewidth=0.1
)
map_ax.axis('off')
map_ax.set_aspect('equal')

# Add colorbar legend below the map
gradient = np.linspace(0, 1, 100).reshape(1, -1)
cbar_ax = inset_axes(ax, width="60%", height="4%",
                     bbox_to_anchor=(0.7, 3.05, 5.6, 0.4),
                     bbox_transform=ax.transData,
                     loc='center')
cbar_ax.imshow(gradient, aspect='auto', cmap='RdYlGn')
cbar_ax.axis('off')

# Colorbar labels
le_min = counties['Mean Life Expectancy'].min()
le_max = counties['Mean Life Expectancy'].max()
ax.text(0.95, 3.15, f'{le_min:.0f} yrs', ha='left', va='center', fontsize=9, color=colors['text_muted'])
ax.text(6.1, 3.15, f'{le_max:.0f} yrs', ha='right', va='center', fontsize=9, color=colors['text_muted'])
ax.text(3.5, 3.15, 'Life Expectancy', ha='center', va='center', fontsize=10, color=colors['text_dark'])

# ============================================================
# RIGHT SIDE: Top 5 Predictors
# ============================================================
predictor_box = FancyBboxPatch(
    (7.0, 3.0), 4.7, 5.0,
    boxstyle="round,pad=0.02,rounding_size=0.15",
    facecolor='#f7fafc',
    edgecolor='#cbd5e0',
    linewidth=1
)
ax.add_patch(predictor_box)

ax.text(9.35, 7.7, 'Top 5 Predictors (SHAP)', ha='center', va='center',
        fontsize=13, fontweight='bold', color=colors['text_dark'])

# Predictor data
predictors = [
    ('Education', 0.95, colors['bar_education']),
    ('Formaldehyde', 0.82, colors['highlight']),
    ('Poverty Rate', 0.68, colors['bar_normal']),
    ('Disability', 0.55, colors['bar_normal']),
    ('Wet Bulb Temp', 0.45, colors['bar_normal']),
]

bar_y_positions = [7.0, 6.2, 5.4, 4.6, 3.8]
bar_height = 0.55
bar_max_width = 3.2

for i, (name, importance, color) in enumerate(predictors):
    y = bar_y_positions[i]
    bar_width = importance * bar_max_width

    bar = FancyBboxPatch(
        (7.4, y - bar_height/2), bar_width, bar_height,
        boxstyle="round,pad=0.01,rounding_size=0.05",
        facecolor=color,
        edgecolor='none',
        alpha=0.9
    )
    ax.add_patch(bar)

    ax.text(7.6, y, f'#{i+1}', ha='left', va='center', fontsize=11,
            fontweight='bold', color=colors['text_light'])

    ax.text(7.4 + bar_width + 0.15, y, name, ha='left', va='center',
            fontsize=12, color=colors['text_dark'],
            fontweight='bold' if color == colors['highlight'] else 'normal')

# Callout for formaldehyde
ax.annotate('', xy=(7.3, 6.2), xytext=(7.1, 6.2),
            arrowprops=dict(arrowstyle='->', color=colors['highlight'], lw=2))
ax.text(7.0, 6.2, 'Environmental\nExposure', ha='right', va='center',
        fontsize=10, color=colors['highlight'], fontweight='bold')

# ============================================================
# BOTTOM: Key Statistics
# ============================================================
stats_box = FancyBboxPatch(
    (0.3, 0.5), 11.4, 2.1,
    boxstyle="round,pad=0.02,rounding_size=0.1",
    facecolor='#edf2f7',
    edgecolor='#cbd5e0',
    linewidth=1
)
ax.add_patch(stats_box)

stat_positions = [2.3, 6.0, 9.7]
stat_labels = ['Model Performance', 'Sample Size', 'Study Period']
stat_values = ['R² = 0.854', '3,047 Counties', '2012-2019']

for x, label, value in zip(stat_positions, stat_labels, stat_values):
    stat_bg = FancyBboxPatch(
        (x - 1.5, 0.75), 3.0, 1.6,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor='white',
        edgecolor='#e2e8f0',
        linewidth=1
    )
    ax.add_patch(stat_bg)

    ax.text(x, 1.95, value, ha='center', va='center',
            fontsize=15, fontweight='bold', color=colors['accent'])
    ax.text(x, 1.25, label, ha='center', va='center',
            fontsize=11, color=colors['text_muted'])

# ============================================================
# Footer
# ============================================================
ax.text(6.0, 0.15, 'XGBoost Regression with Bayesian Optimization  •  43 Environmental & Socioeconomic Features',
        ha='center', va='center', fontsize=10, color=colors['text_muted'], style='italic')

# Save
plt.savefig('/Users/samyakshrestha/Projects/Life Expectancy Project/paper/Figures/visual_abstract.png',
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.savefig('/Users/samyakshrestha/Projects/Life Expectancy Project/paper/Figures/visual_abstract.pdf',
            bbox_inches='tight', facecolor='white', edgecolor='none')
print("Visual abstract saved to paper/Figures/visual_abstract.png and .pdf")
