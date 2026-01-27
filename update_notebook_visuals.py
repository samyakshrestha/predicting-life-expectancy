import json
import os

nb_path = 'notebooks_clean/09_xgboost_bayesian_optimization_run3.ipynb'

if not os.path.exists(nb_path):
    print(f"Error: File not found at {nb_path}")
    exit(1)

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

modifications = 0

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        new_source = []
        for line in cell['source']:
            # DPI update
            if 'DPI = 300' in line:
                new_line = line.replace('DPI = 300', 'DPI = 600')
                new_source.append(new_line)
                modifications += 1
            # SHAP update
            elif 'shap.dependence_plot(' in line and 'interaction_index' not in line:
                # We expect the line to end with "show=False)\n" or similar.
                # We want to inject interaction_index=None.
                if 'show=False)' in line:
                    new_line = line.replace('show=False)', 'show=False, interaction_index=None)')
                    new_source.append(new_line)
                    modifications += 1
                else:
                    # If the line doesn't match expected pattern, print warning but don't break
                    print(f"Warning: Found shap.dependence_plot but couldn't safely replace: {line.strip()}")
                    new_source.append(line)
            else:
                new_source.append(line)
        cell['source'] = new_source

# Notebooks usually use an indentation of 1 space
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print(f"Successfully modified {modifications} lines in the notebook.")
