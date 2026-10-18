# Sri Lankan Retail Price Intelligence Dashboard

An end-to-end data analytics project that analyzes retail price trends, price fluctuations, and volatility of essential consumer items in Colombo, Sri Lanka, from 2020 to 2024. Built using Python, Pandas, NumPy, Plotly, and Streamlit, the project transforms raw weekly retail price data into meaningful insights through a structured data pipeline and an interactive dashboard.

**Live Dashboard:** [View Dashboard](https://sri-lankan-retail-price-intelligence-yzvnq4buekmvh3msfnynkr.streamlit.app/)

**GitHub Repository:** [Sri Lankan Retail Price Intelligence](https://github.com/Ridmika23/Sri-Lankan-Retail-Price-Intelligence)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Business Problem](#business-problem)
- [Project Objectives](#project-objectives)
- [Dataset](#dataset)
- [Key Features](#key-features)
- [Analytical Questions](#analytical-questions)
- [Key Performance Metrics](#key-performance-metrics)
- [Key Findings](#key-findings)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Data Pipeline](#data-pipeline)
- [Installation and Setup](#installation-and-setup)
- [Execution Instructions](#execution-instructions)
- [Testing and Quality Assurance](#testing-and-quality-assurance)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Project Overview

The Sri Lankan Retail Price Intelligence Dashboard is a data analytics solution designed to explore historical price movements of essential consumer goods in Colombo, Sri Lanka.

The project implements a structured data processing pipeline to ingest, validate, clean, and transform raw weekly retail price records. The processed data is then used to calculate analytical metrics and generate interactive visualizations.

The dashboard enables users to investigate historical price trends, compare average prices, examine price ranges, and identify items with relatively high price volatility.

The project also emphasizes data quality, reproducibility, and automated testing to support reliable data processing and analysis.

## Business Problem

Sri Lanka has experienced significant economic changes and fluctuations in the cost of living in recent years. Monitoring the prices of essential consumer goods is important for understanding price movements and their potential impact on consumers, businesses, and policymakers.

However, raw retail price datasets may contain inconsistent date formats, missing values, and other data quality issues that make analysis difficult.

This project addresses these challenges by developing a reproducible data pipeline and an interactive dashboard that transforms raw retail price data into structured information for historical analysis and comparison.

## Project Objectives

- Ingest and validate raw weekly retail price data.
- Clean and standardize inconsistent date formats, including Week-To-Date values.
- Handle missing values and improve data consistency.
- Calculate price changes, price ranges, and price volatility.
- Analyze historical retail price trends from 2020 to 2024.
- Develop an interactive dashboard for data exploration and visualization.
- Build a reproducible data processing pipeline.
- Implement automated tests to validate data processing and dashboard functionality.

## Dataset

- **Source:** Publicly available Sri Lankan retail price dataset covering Colombo.
- **Time Period:** 2020–2024.
- **Data Frequency:** Weekly.
- **Data Fields:** Item identifiers or names, average prices, low prices, high prices, and weekly date identifiers, depending on the original dataset schema.

The dataset supports longitudinal analysis of retail prices and comparisons between individual consumer items over time.

The original dataset and its licensing information should be referenced according to the source documentation.

## Key Features

### Data Ingestion and Validation

- Load raw retail price data from CSV files.
- Validate the dataset structure and required columns.
- Identify potential data quality issues before processing.

### Data Cleaning and Transformation

- Standardize inconsistent weekly date formats.
- Convert columns into appropriate data types.
- Handle missing and invalid values.
- Transform raw records into a structured dataset for analysis.

### Retail Price Analysis

- Analyze historical average price trends.
- Compare prices across individual consumer items.
- Calculate high-low price spreads.
- Measure relative price volatility.
- Compare the latest recorded prices with historical averages.

### Interactive Dashboard

- Visualize historical price trends using Plotly.
- Explore retail price data through Streamlit controls.
- Compare items and their price movements.
- Present analytical metrics through interactive visualizations.

### Automated Testing

- Test data loading and validation functions.
- Verify data cleaning and transformation logic.
- Validate analytical calculations.
- Test supported dashboard functionality using Streamlit AppTest.

## Analytical Questions

The project investigates the following questions:

1. How have the prices of essential consumer goods changed between 2020 and 2024?
2. Which items demonstrate the highest price volatility?
3. What is the difference between the recorded high and low prices of individual items?
4. How do the latest available prices compare with historical averages?
5. Which items experience the largest week-over-week percentage price changes?

## Key Performance Metrics

| Metric | Description |
|---|---|
| Average Price (LKR) | Mean recorded retail price of an item for a given period. |
| Price Range (LKR) | Difference between the recorded high and low prices for a given observation. |
| Price Volatility | Relative price variability measured using the coefficient of variation. |
| Average Weekly Percentage Change | Average week-over-week percentage change in an item's average price. |
| Latest Recorded Price | Most recent available average price for an item. |
| Historical Average Price | Average recorded price across the selected historical period. |

### Price Volatility

The coefficient of variation (CV) measures price variability relative to the mean.

\[
CV = \frac{\text{Standard Deviation}}{\text{Mean Price}}
\]

A higher coefficient of variation indicates greater relative variability in an item's prices over the selected period.

### Weekly Percentage Change

\[
\text{Percentage Change} =
\frac{P_t-P_{t-1}}{P_{t-1}}\times100
\]

Where:

- \(P_t\) represents the current week's average price.
- \(P_{t-1}\) represents the previous week's average price.

## Key Findings

The following areas are investigated through exploratory data analysis and dashboard visualizations:

- **Historical Price Trends:** Changes in the prices of essential consumer goods over the study period.
- **Price Volatility:** Items with the highest relative price variability.
- **Price Range Analysis:** Differences between recorded high and low prices.
- **Recent Price Movements:** Comparisons between the latest recorded prices and historical averages.

Specific findings, including item names, percentage changes, and price values, should be added after validating the final analytical results.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Data processing and application development |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical calculations |
| Plotly | Interactive data visualization |
| Streamlit | Dashboard development |
| Pytest | Automated testing |
| Streamlit AppTest | Dashboard testing |
| Git | Version control |
| GitHub | Source code management and collaboration |

## Project Structure

```text
Sri-Lankan-Retail-Price-Intelligence/
|
├── data/
│   ├── raw/                 # Original datasets
│   └── processed/           # Cleaned datasets
│
├── dashboard/
│   └── app.py               # Streamlit dashboard
│
├── src/
│   ├── data_loader.py       # Data ingestion and validation
│   └── cleaning.py          # Data cleaning and transformation
│
├── tests/                   # Automated test suite
│
├── scripts/
│   └── run_cleaning.py      # Data cleaning pipeline
│
├── reports/                 # QA and data quality reports
│
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
└── .gitignore               # Git exclusion rules
```

The structure above represents the intended organization. Update the filenames and directories if the actual repository differs.

## Data Pipeline

The project follows a structured workflow to transform raw data into analytical insights.

```text
Raw Retail Price Dataset
          |
          v
    Data Ingestion
          |
          v
   Schema Validation
          |
          v
 Data Cleaning and
    Standardization
          |
          v
  Metric Calculation
          |
          v
  Processed Dataset
          |
          v
 Interactive Dashboard
          |
          v
   Analytical Insights
```

Separating data processing from dashboard development improves maintainability, testability, and reproducibility.

## Installation and Setup

### Prerequisites

Ensure that the following software is installed:

- Python 3.11 or later
- Git
- Visual Studio Code or another code editor

### 1. Clone the Repository

```bash
git clone https://github.com/Ridmika23/Sri-Lankan-Retail-Price-Intelligence.git
cd Sri-Lankan-Retail-Price-Intelligence
```

### 2. Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Execution Instructions

### 1. Prepare the Dataset

Place the original dataset in the expected location:

```text
data/raw/dataset.csv
```

Ensure that the filename and column structure match the requirements of the data loading and cleaning scripts.

### 2. Execute the Data Cleaning Pipeline

```bash
python scripts/run_cleaning.py
```

The pipeline is expected to generate the following processed dataset:

```text
data/processed/retail_prices_cleaned.csv
```

### 3. Run Automated Tests

```bash
python -m pytest -v
```

This command executes the available tests for data validation, transformation, analytical calculations, and dashboard functionality.

### 4. Launch the Dashboard

```bash
python -m streamlit run dashboard/app.py
```

Open the following address in your browser:

http://localhost:8501

The dashboard can then be used to explore the available retail price records and visualizations.

## Testing and Quality Assurance

Data quality and calculation accuracy are important for producing reliable analytical insights.

The project uses the following testing approaches:

- **Unit Testing:** Verifies the behavior of individual data processing functions.
- **Data Validation Testing:** Checks the dataset structure, required fields, and relevant data constraints.
- **Calculation Testing:** Validates price range, percentage change, and volatility calculations.
- **Dashboard Testing:** Uses Streamlit AppTest to verify supported dashboard behavior.

Run the test suite using:

```bash
python -m pytest -v
```

Test results and coverage metrics should be documented after running the tests against the current codebase.

## Limitations

- **Geographic Coverage:** The dataset focuses on Colombo and may not represent retail prices across the entire country.
- **Absence of Sales Volume:** Revenue, profit, and consumer demand cannot be reliably calculated without sales volume information.
- **Missing Price Boundaries:** Missing high or low price values are excluded from the relevant calculations rather than automatically imputed.
- **Date Approximation:** Weekly identifiers such as `2020-01-W1` may be mapped to approximate dates instead of exact observation dates.
- **Limited Product Classification:** The absence of detailed product categories or market identifiers restricts category-level and market-level comparisons.
- **Historical Scope:** The dataset covers 2020–2024 and does not necessarily reflect current retail prices.

## Future Improvements

- Integrate additional datasets covering different regions and retail markets in Sri Lanka.
- Incorporate sales volume and demand data for broader business analysis.
- Implement time-series forecasting models such as ARIMA or Prophet.
- Introduce anomaly detection to identify unusual price movements.
- Configure continuous integration using GitHub Actions to run automated tests on code changes.
- Automate data updates and dashboard refreshes.
- Add additional filtering, reporting, and data export capabilities.
- Expand data quality monitoring and automated test coverage.

## Author

**Ridmika Yohani**

Final-year Software Engineering undergraduate at Sri Lanka Technology Campus, with interests in data analytics, artificial intelligence, and software quality assurance.

- **GitHub:** [Ridmika23](https://github.com/Ridmika23)
- **Project Repository:** [Sri Lankan Retail Price Intelligence](https://github.com/Ridmika23/Sri-Lankan-Retail-Price-Intelligence)
- **Live Dashboard:** [Sri Lankan Retail Price Intelligence Dashboard](https://sri-lankan-retail-price-intelligence-yzvnq4buekmvh3msfnynkr.streamlit.app/)

---
