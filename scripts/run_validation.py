import sys
from pathlib import Path

# Add src to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from src.data_loader import load_data, validate_data, generate_quality_report

def main():
    raw_data_path = Path("data/raw/dataset.csv")
    report_path = Path("reports/data_quality_report.md")
    
    print(f"Loading data from {raw_data_path}...")
    df = load_data(raw_data_path)
    
    print("Validating data...")
    report = validate_data(df)
    
    print("Generating quality report...")
    generate_quality_report(report, report_path)
    
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    main()
