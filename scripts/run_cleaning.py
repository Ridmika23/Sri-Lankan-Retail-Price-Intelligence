import sys
import pandas as pd
from pathlib import Path

# Add src to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from src.cleaning import clean_data, generate_cleaning_report

def main():
    raw_data_path = Path("data/raw/dataset.csv")
    clean_data_path = Path("data/processed/retail_prices_cleaned.csv")
    report_path = Path("reports/cleaning_report.md")
    
    print(f"Loading raw data from {raw_data_path}...")
    try:
        df_raw = pd.read_csv(raw_data_path)
    except FileNotFoundError:
        print(f"Error: {raw_data_path} not found.")
        sys.exit(1)
        
    print("Cleaning data...")
    df_clean = clean_data(df_raw)
    
    print(f"Saving cleaned data to {clean_data_path}...")
    clean_data_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(clean_data_path, index=False)
    
    print("Generating cleaning report...")
    generate_cleaning_report(df_raw, df_clean, report_path)
    
    print(f"Process complete. Report saved to {report_path}")

if __name__ == "__main__":
    main()
