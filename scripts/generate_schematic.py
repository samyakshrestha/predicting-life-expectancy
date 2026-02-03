"""
Generate a clean methodology schematic for the Life Expectancy paper.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Set up the figure
fig, ax = plt.subplots(1, 1, figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')

# Color palette - soft, professional colors
colors = {
    'ihme': '#E8F4FD',       # Light blue
    'census': '#FDF2E8',      # Light orange
    'cams': '#E8FDF2',        # Light green
    'fao': '#F2E8FD',         # Light purple
    'process': '#F5F5F5',     # Light gray
    'model': '#FFF8E8',       # Light yellow
    'results': '#FFE8E8',     # Light red/pink
    'border': '#555555',      # Dark gray for borders
    'arrow': '#888888',       # Medium gray for arrows
    'text': '#333333',        # Dark text
}

def draw_box(ax, x, y, width, height, color, title, subtitle='', border_color='#555555'):
    """Draw a rounded box with title and subtitle."""
    box = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.03,rounding_size=0.15",
        facecolor=color,
        edgecolor=border_color,
        linewidth=1.5
    )
    ax.add_patch(box)

    # Title
    ax.text(x + width/2, y + height/2 + 0.15, title,
            ha='center', va='center', fontsize=10, fontweight='bold',
            color=colors['text'])

    # Subtitle
    if subtitle:
        ax.text(x + width/2, y + height/2 - 0.25, subtitle,
                ha='center', va='center', fontsize=8,
                color='#666666', style='italic')

def draw_arrow(ax, start, end, color='#888888'):
    """Draw a simple arrow."""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

# Section headers
ax.text(1.3, 7.5, 'DATA SOURCES', ha='center', va='center', fontsize=12,
        fontweight='bold', color='#444444')
ax.text(5.0, 7.5, 'PROCESSING', ha='center', va='center', fontsize=12,
        fontweight='bold', color='#444444')
ax.text(8.5, 7.5, 'MODELING', ha='center', va='center', fontsize=12,
        fontweight='bold', color='#444444')
ax.text(12.0, 7.5, 'RESULTS', ha='center', va='center', fontsize=12,
        fontweight='bold', color='#444444')

# Data source boxes - with descriptive category labels
draw_box(ax, 0.3, 5.8, 2.0, 1.2, colors['ihme'], 'Life Expectancy', 'Target Variable')
draw_box(ax, 0.3, 4.2, 2.0, 1.2, colors['census'], 'Socioeconomic', '10 Variables')
draw_box(ax, 0.3, 2.6, 2.0, 1.2, colors['cams'], 'Atmospheric', '26 Variables')
draw_box(ax, 0.3, 1.0, 2.0, 1.2, colors['fao'], 'Livestock', '7 Variables')

# Processing box
draw_box(ax, 3.8, 2.8, 2.4, 3.0, colors['process'], '', '')
ax.text(5.0, 5.2, 'Feature', ha='center', va='center', fontsize=10,
        fontweight='bold', color=colors['text'])
ax.text(5.0, 4.8, 'Engineering', ha='center', va='center', fontsize=10,
        fontweight='bold', color=colors['text'])
ax.text(5.0, 4.1, '• County aggregation', ha='center', va='center',
        fontsize=8, color='#666666')
ax.text(5.0, 3.7, '• Correlation filtering', ha='center', va='center',
        fontsize=8, color='#666666')
ax.text(5.0, 3.3, '• 43 final features', ha='center', va='center',
        fontsize=8, color='#666666')

# Model box
draw_box(ax, 7.0, 2.8, 3.0, 3.0, colors['model'], '', '')
ax.text(8.5, 5.2, 'XGBoost', ha='center', va='center', fontsize=10,
        fontweight='bold', color=colors['text'])
ax.text(8.5, 4.8, 'Regression', ha='center', va='center', fontsize=10,
        fontweight='bold', color=colors['text'])
ax.text(8.5, 4.1, '• Bayesian optimization', ha='center', va='center',
        fontsize=8, color='#666666')
ax.text(8.5, 3.7, '• GroupKFold CV', ha='center', va='center',
        fontsize=8, color='#666666')
ax.text(8.5, 3.3, '• SHAP interpretation', ha='center', va='center',
        fontsize=8, color='#666666')

# Results box
draw_box(ax, 10.7, 2.8, 2.6, 3.0, colors['results'], '', '')
ax.text(12.0, 5.2, 'Key Findings', ha='center', va='center', fontsize=10,
        fontweight='bold', color=colors['text'])
ax.text(12.0, 4.4, '#1 Education', ha='center', va='center',
        fontsize=9, color='#444444')
ax.text(12.0, 4.0, '#2 Formaldehyde', ha='center', va='center',
        fontsize=9, fontweight='bold', color='#c41e3a')  # Highlighted
ax.text(12.0, 3.6, '#3 Poverty Rate', ha='center', va='center',
        fontsize=9, color='#444444')
ax.text(12.0, 3.2, 'Test R² = 0.854', ha='center', va='center',
        fontsize=8, color='#666666', style='italic')

# Arrows from data sources to processing
draw_arrow(ax, (2.3, 6.4), (3.8, 4.8))
draw_arrow(ax, (2.3, 4.8), (3.8, 4.3))
draw_arrow(ax, (2.3, 3.2), (3.8, 3.8))
draw_arrow(ax, (2.3, 1.6), (3.8, 3.3))

# Arrow from processing to model
draw_arrow(ax, (6.2, 4.3), (7.0, 4.3))

# Arrow from model to results
draw_arrow(ax, (10.0, 4.3), (10.7, 4.3))

# Add sample info at bottom
ax.text(7.0, 0.5, '3,047 U.S. Counties  •  2012-2019  •  24,487 County-Year Observations',
        ha='center', va='center', fontsize=9, color='#666666', style='italic')

# Add title
ax.text(7.0, 7.9, 'Study Overview', ha='center', va='center',
        fontsize=14, fontweight='bold', color='#333333')

plt.tight_layout()
plt.savefig('/Users/samyakshrestha/Projects/Life Expectancy Project/paper/Figures/fig0_methodology_schematic.png',
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.savefig('/Users/samyakshrestha/Projects/Life Expectancy Project/paper/Figures/fig0_methodology_schematic.pdf',
            bbox_inches='tight', facecolor='white', edgecolor='none')
print("Schematic saved to paper/Figures/fig0_methodology_schematic.png and .pdf")
