import pandas as pd
import numpy as np
from pathlib import Path

REQUIRED_COLUMNS = [
    'Week',
    'Item',
    'Unit',
    'Avg Price (Rs.)',
    'Price Range - low (Rs.)',
    'Price Range - High (Rs.)'
]

def load_data(filepath: str | Path) -> pd.DataFrame:
    """Loads raw dataset from the given filepath."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")
    
    df = pd.read_csv(path)
    return df

def validate_data(df: pd.DataFrame) -> dict:
    """Validates the dataset for quality issues."""
    report = {
        'total_rows': len(df),
        'missing_columns': [],
        'missing_values': {},
        'negative_prices': 0,
        'invalid_dates': 0,
        'duplicate_rows': int(df.duplicated().sum()),
        'invalid_units': []
    }
    
    # Check columns
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    report['missing_columns'] = missing
    
    if missing:
        return report # Cannot proceed with further validation if columns are missing

    # Missing values
    report['missing_values'] = df[REQUIRED_COLUMNS].isnull().sum().to_dict()
    
    # Negative prices
    numeric_cols = ['Avg Price (Rs.)', 'Price Range - low (Rs.)', 'Price Range - High (Rs.)']
    for col in numeric_cols:
        try:
            # Convert to numeric, errors='coerce' turns non-numeric to NaN
            numeric_series = pd.to_numeric(df[col], errors='coerce')
            report['negative_prices'] += int((numeric_series < 0).sum())
        except Exception:
            pass

    # Invalid dates (Week should ideally follow "YYYY-MM-W#")
    # For a simple check, just see if it contains "-W"
    invalid_dates = df[~df['Week'].astype(str).str.contains(r'^\d{4}-\d{2}-W\d$', regex=True, na=False)]
    report['invalid_dates'] = len(invalid_dates)

    # Units overview (Not necessarily invalid, just collecting unique ones for report)
    report['invalid_units'] = df['Unit'].dropna().unique().tolist()

    return report

def generate_quality_report(report: dict, output_path: str | Path):
    """Generates a markdown report for data quality."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# Data Quality Report\n\n")
        f.write(f"- **Total Rows:** {report.get('total_rows', 0)}\n")
        f.write(f"- **Duplicate Rows:** {report.get('duplicate_rows', 0)}\n")
        
        if report.get('missing_columns'):
            f.write(f"## Missing Columns\n**CRITICAL:** The following required columns are missing: {', '.join(report['missing_columns'])}\n")
            return
            
        f.write("## Missing Values\n")
        for col, count in report.get('missing_values', {}).items():
            f.write(f"- `{col}`: {count} missing\n")
            
        f.write(f"\n## Data Integrity\n")
        f.write(f"- **Negative Prices Found:** {report.get('negative_prices', 0)}\n")
        f.write(f"- **Invalid Date Formats (Expected YYYY-MM-W#):** {report.get('invalid_dates', 0)}\n")
        
        f.write("\n## Units Present\n")
        f.write(", ".join(map(str, report.get('invalid_units', []))) + "\n")
