import csv
import collections
from pathlib import Path

def main():
    path = Path('data/raw/dataset.csv')
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
        
    print(f"Columns: {headers}")
    print(f"Total Rows: {len(rows)}")
    
    missing = collections.defaultdict(int)
    dates = set()
    neg_prices = 0
    
    # Check duplicates
    dupes = len(rows) - len(set(tuple(x) for x in rows))
    print(f"Duplicate rows: {dupes}")
    
    for row in rows:
        dates.add(row[0])
        for i, val in enumerate(row):
            if not val.strip():
                missing[headers[i]] += 1
            if i >= 3 and val.strip():
                try:
                    if float(val) < 0:
                        neg_prices += 1
                except ValueError:
                    pass
                    
    print(f"Date range: {min(dates)} to {max(dates)}")
    print(f"Missing values by column: {dict(missing)}")
    print(f"Negative prices: {neg_prices}")
    
    # Save a mock report since pandas failed
    report_path = Path("reports/data_quality_report.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as rf:
        rf.write("# Data Quality Report\n\n")
        rf.write(f"- **Total Rows:** {len(rows)}\n")
        rf.write(f"- **Duplicate Rows:** {dupes}\n")
        rf.write(f"- **Date Range:** {min(dates)} to {max(dates)}\n")
        rf.write(f"## Missing Values\n")
        for k, v in missing.items():
            rf.write(f"- {k}: {v}\n")
    print("Report saved to reports/data_quality_report.md")

if __name__ == '__main__':
    main()
