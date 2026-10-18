# Sri Lankan Retail Price Intelligence Dashboard

A professional data analytics pipeline and interactive Streamlit dashboard tracking the retail prices of essential consumer items in Colombo, Sri Lanka (2020-2024).

## Business Problem
Sri Lanka has faced significant economic volatility in recent years, leading to rapid fluctuations in the cost of living. Monitoring the retail prices of essential consumer items is crucial for policy-makers, businesses, and consumers to understand inflation trends, market stability, and purchasing power.

## Objectives
- Ingest and validate raw weekly retail price data.
- Clean and standardize non-standard date formats (e.g., Week-To-Date strings).
- Calculate key longitudinal metrics including percentage change and price volatility.
- Build a robust, reproducible data pipeline with comprehensive automated testing.
- Develop an interactive dashboard for intuitive visual analysis of price trends, comparisons, and volatility.

## Dataset
- **Source:** Publicly available Sri Lankan retail-price dataset covering Colombo.
- **Dimensions:** Weekly records of retail items including average, low, and high prices. 

## Analytical Questions
1. How have the prices of essential goods trended over the 2020-2024 period?
2. Which consumer items exhibit the highest price volatility?
3. What is the standard price range (high-low spread) for individual items?
4. How do current latest prices compare to historical averages?

## Key Metrics
- **Average Price (LKR):** The mean weekly retail price per item.
- **Price Range (LKR):** The absolute spread between the maximum and minimum recorded price for a given week.
- **Price Volatility (Coefficient of Variation):** The relative instability of an item's price, calculated as the standard deviation divided by the mean.
- **Avg Weekly % Change:** The week-over-week percentage change in average price for an item.

## Key Findings
*Note: The following findings are based on the initial exploratory analysis. Replace with finalized metrics.*
- **[FINDING 1 PLACEHOLDER - e.g., Rice prices spiked sharply in Mid-2022 due to macro-economic events.]**
- **[FINDING 2 PLACEHOLDER - e.g., Item X showed the highest volatility with a Coefficient of Variation exceeding Y%.]**
- **[FINDING 3 PLACEHOLDER - e.g., Most items show a steady upward trend in baseline prices over the 4-year period.]**

## Limitations
- **No Category/Market Information:** The dataset lacks explicit product categories or market locations, restricting analysis to item-level trends.
- **No Volume Data:** Revenue, profit, and market demand cannot be calculated as sales volume is unknown.
- **Missing Ranges:** Missing 'low' or 'high' price boundaries are ignored rather than imputed.
- **Week Parsing Assumptions:** Original week identifiers (e.g., '2020-01-W1') are approximated to the first of the month, adding 7 days per subsequent week.

## Technology Stack
- **Language:** Python 3.11+
- **Data Processing:** `pandas`, `numpy`
- **Visualization:** `plotly`
- **Dashboard UI:** `streamlit`
- **Testing & QA:** `pytest`, Streamlit `AppTest`

## Folder Structure
```text
sri-lankan-retail-price-dashboard/
├── data/
│   ├── raw/             # Original immutable datasets
│   └── processed/       # Cleaned, transformed data ready for analysis
├── dashboard/
│   └── app.py           # Streamlit dashboard application
├── src/
│   ├── data_loader.py   # Ingestion and schema validation logic
│   └── cleaning.py      # Data cleaning and transformation functions
├── tests/               # Pytest suite (unit and UI AppTest)
├── scripts/             # Pipeline execution automation
├── reports/             # QA, data quality, and testing reports
└── README.md
```

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/sri-lankan-retail-price-dashboard.git
   cd sri-lankan-retail-price-dashboard
   ```

2. **Create and activate a virtual environment:**
   - **Windows:**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate
     ```
   - **macOS/Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Execution Instructions

### 1. Data Setup & Pipeline
Ensure your raw dataset is located at `data/raw/dataset.csv`. Then, run the cleaning pipeline to validate and transform the data:
```bash
python scripts/run_cleaning.py
```
This generates the `data/processed/retail_prices_cleaned.csv` file required by the dashboard.

### 2. Test Execution
Run the full test suite (including data validation, transformation, and UI tests) to ensure the pipeline is healthy:
```bash
python -m pytest -v
```

### 3. Dashboard Execution
Start the interactive Streamlit application:
```bash
python -m streamlit run dashboard/app.py
```
The dashboard will be available in your browser at `http://localhost:8501`.

## Future Improvements
- Integrate a secondary dataset containing market locations or sales volume data.
- Add predictive forecasting models (e.g., ARIMA or Prophet) to predict short-term price trends.
- Implement an automated CI/CD pipeline using GitHub Actions to run the pytest suite on every push.

