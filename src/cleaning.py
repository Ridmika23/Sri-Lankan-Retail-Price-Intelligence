import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans and transforms raw retail price data."""
    df_clean = df.copy()

    # 1. Standardize column names internally
    col_mapping = {
        'Week': 'original_week',
        'Item': 'item',
        'Unit': 'unit',
        'Avg Price (Rs.)': 'avg_price',
        'Price Range - low (Rs.)': 'min_price',
        'Price Range - High (Rs.)': 'max_price'
    }
    df_clean = df_clean.rename(columns=col_mapping)

    # 2. Preserve original week, convert to reliable date
    def parse_week(week_str):
        if pd.isna(week_str):
            return pd.NaT
        try:
            parts = str(week_str).split('-')
            if len(parts) == 3 and parts[2].startswith('W'):
                year = int(parts[0])
                month = int(parts[1])
                week_of_month = int(parts[2].replace('W', ''))
                # Approximate date (1st of month + (week-1)*7 days)
                day = min(1 + (week_of_month - 1) * 7, 28) # Cap at 28 to avoid month overflow
                return pd.Timestamp(year=year, month=month, day=day)
        except Exception:
            pass
        return pd.NaT

    df_clean['date'] = df_clean['original_week'].apply(parse_week)

    # 3. Clean item and unit (strip whitespace, uppercase unit to standardize if needed)
    df_clean['item'] = df_clean['item'].astype(str).str.strip()
    df_clean['unit'] = df_clean['unit'].astype(str).str.strip()

    # 4. Convert prices to numeric
    price_cols = ['avg_price', 'min_price', 'max_price']
    for col in price_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    # 5. Derived fields
    df_clean['year'] = df_clean['date'].dt.year
    df_clean['month'] = df_clean['date'].dt.month
    df_clean['quarter'] = df_clean['date'].dt.quarter
    df_clean['week_number'] = df_clean['date'].dt.isocalendar().week

    # Price range
    df_clean['price_range'] = df_clean['max_price'] - df_clean['min_price']

    # Sort to calculate accurate changes
    df_clean = df_clean.sort_values(by=['item', 'date'])

    # Calculate price change and percentage change safely
    df_clean['prev_price'] = df_clean.groupby('item')['avg_price'].shift(1)
    df_clean['price_change'] = df_clean['avg_price'] - df_clean['prev_price']
    
    # Safe percentage calculation: handle division by zero
    def safe_pct_change(row):
        if pd.isna(row['prev_price']) or row['prev_price'] == 0:
            return np.nan
        return (row['price_change'] / row['prev_price']) * 100
        
    df_clean['price_change_percentage'] = df_clean.apply(safe_pct_change, axis=1)

    # Drop temporary column
    df_clean = df_clean.drop(columns=['prev_price'])

    return df_clean

def generate_cleaning_report(df_raw: pd.DataFrame, df_clean: pd.DataFrame, output_path: str):
    """Generates a markdown report outlining data transformations."""
    import json
    from pathlib import Path
    
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# Data Cleaning Report\n\n")
        f.write(f"- **Initial Rows:** {len(df_raw)}\n")
        f.write(f"- **Final Rows:** {len(df_clean)}\n")
        
        f.write("\n## Missing Values (After Cleaning)\n")
        missing = df_clean.isnull().sum().to_dict()
        for k, v in missing.items():
            f.write(f"- {k}: {v}\n")
            
        f.write("\n## Column Transformations\n")
        f.write("- Standardized column names.\n")
        f.write("- Parsed `original_week` into `date`.\n")
        f.write("- Derived `year`, `month`, `quarter`, `week_number`.\n")
        f.write("- Added `price_range`.\n")
        f.write("- Calculated `price_change` and `price_change_percentage` safely.\n")
