import pandas as pd
import xgboost as xgb
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import r2_score

# Load data
print("Loading data...")
df = pd.read_csv('data_cleaned/combined_final/final_combined_all_variables_reduced.csv')
X = df.drop(columns=['County', 'State', 'Year', 'Fips', 'Mean Life Expectancy'])
y = df['Mean Life Expectancy']
groups = df['Fips']

# Standard Split (Leakage-prone) - simulating your previous results
from sklearn.model_selection import train_test_split
X_train_bad, X_test_bad, y_train_bad, y_test_bad = train_test_split(X, y, test_size=0.2, random_state=42)

model_bad = xgb.XGBRegressor(n_jobs=-1, random_state=42)
model_bad.fit(X_train_bad, y_train_bad)
r2_bad = r2_score(y_test_bad, model_bad.predict(X_test_bad))
print(f"\n[Old Method] Random Split R2: {r2_bad:.4f} (This allows same county in train & test)")

# Group Split (Rigorous) - simulating new method
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, test_idx = next(gss.split(X, y, groups=groups))
X_train_good, X_test_good = X.iloc[train_idx], X.iloc[test_idx]
y_train_good, y_test_good = y.iloc[train_idx], y.iloc[test_idx]

model_good = xgb.XGBRegressor(n_jobs=-1, random_state=42)
model_good.fit(X_train_good, y_train_good)
r2_good = r2_score(y_test_good, model_good.predict(X_test_good))
print(f"[New Method] Group Split R2:  {r2_good:.4f} (Counties in test set are NEVER seen in training)")

diff = r2_bad - r2_good
print(f"\nDifference: {diff:.4f}")
if diff > 0.1:
    print("VERDICT: Significant leakage detected. Using the old result is unsafe.")
else:
    print("VERDICT: Result is robust! The exact method matters less than we thought.")
