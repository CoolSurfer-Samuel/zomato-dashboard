import pandas as pd
import numpy as np
from pathlib import Path

# ── 1. Load ──────────────────────────────────────────────────────────────────
df = pd.read_csv(Path('data') / 'zomato.csv', encoding='latin-1')
print(f"Raw shape: {df.shape}")

# ── 2. Rename columns to friendly names ──────────────────────────────────────
df.rename(columns={
    'Restaurant ID':        'restaurant_id',
    'Restaurant Name':      'name',
    'Country Code':         'country_code',
    'City':                 'city',
    'Address':              'address',
    'Locality':             'location',
    'Locality Verbose':     'location_verbose',
    'Longitude':            'longitude',
    'Latitude':             'latitude',
    'Cuisines':             'cuisines',
    'Average Cost for two': 'approx_cost',
    'Currency':             'currency',
    'Has Table booking':    'book_table',
    'Has Online delivery':  'online_order',
    'Is delivering now':    'delivering_now',
    'Switch to order menu': 'order_menu',
    'Price range':          'price_range',
    'Aggregate rating':     'rate',
    'Rating color':         'rating_color',
    'Rating text':          'rating_text',
    'Votes':                'votes',
}, inplace=True)

print(f"Renamed columns: {df.columns.tolist()}")

# ── 3. Fix ratings (already numeric, just handle 0s = no rating yet) ─────────
df['rate'] = pd.to_numeric(df['rate'], errors='coerce')
df['rate'] = df['rate'].replace(0, np.nan)

# ── 4. Fix cost ───────────────────────────────────────────────────────────────
df['approx_cost'] = pd.to_numeric(df['approx_cost'], errors='coerce')

# ── 5. Fix votes ──────────────────────────────────────────────────────────────
df['votes'] = pd.to_numeric(df['votes'], errors='coerce').fillna(0).astype(int)

# ── 6. Fix boolean columns (Yes/No → True/False) ─────────────────────────────
for col in ['book_table', 'online_order', 'delivering_now']:
    df[col] = df[col].map({'Yes': True, 'No': False})

# ── 7. Drop rows missing critical fields ─────────────────────────────────────
before = len(df)
df.dropna(subset=['rate', 'location', 'cuisines', 'approx_cost'], inplace=True)
after = len(df)
print(f"\nDropped {before - after} rows with nulls in key columns")
print(f"Clean shape: {df.shape}")

# ── 8. Sanity checks ──────────────────────────────────────────────────────────
print(f"\nRate range:  {df['rate'].min():.1f} – {df['rate'].max():.1f}")
print(f"Cost range:  {df['approx_cost'].min():.0f} – {df['approx_cost'].max():.0f}")
print(f"Cities:      {df['city'].nunique()} unique")
print(f"Countries:   {df['country_code'].nunique()} unique")
print(f"Cuisines:    {df['cuisines'].nunique()} unique")

print(f"\nSample (5 rows):")
print(df[['name','city','rate','approx_cost',
          'online_order','book_table','cuisines']].head())

# ── 9. Save ───────────────────────────────────────────────────────────────────
df.to_csv(Path('data') / 'zomato_clean.csv', index=False)
print("\nSaved → data/zomato_clean.csv")