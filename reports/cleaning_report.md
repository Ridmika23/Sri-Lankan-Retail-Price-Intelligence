# Data Cleaning Report

- **Initial Rows:** 22449
- **Final Rows:** 22449

## Missing Values (After Cleaning)
- original_week: 0
- item: 0
- unit: 0
- avg_price: 37
- min_price: 1005
- max_price: 1005
- date: 0
- year: 0
- month: 0
- quarter: 0
- week_number: 0
- price_range: 1007
- price_change: 187
- price_change_percentage: 189

## Column Transformations
- Standardized column names.
- Parsed `original_week` into `date`.
- Derived `year`, `month`, `quarter`, `week_number`.
- Added `price_range`.
- Calculated `price_change` and `price_change_percentage` safely.
