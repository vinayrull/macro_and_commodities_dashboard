# Macroeconomic & Commodities Dashboard

## Overview

This project uses Python to collect, process, and store macroeconomic and commodity data from public APIs, which is then visualised in an Power BI dashboard.

---

## Files Required

- **macro_and_commodities_dashboard.pbix** – Power BI dashboard
- **macro_and_commodities_dashboard.py** – Python script  
- **commodities_data.csv**
- **macro_data.csv**  

---

## How to Run

1. Place `macro_and_commodities_dashboard.pbix` and `macro_and_commodities_dashboard.py` in the same folder.
2. Inside this folder, create a subfolder named `data`.
3. Place `commodities_data.csv` and `macro_data.csv` inside the `data` folder.
4. Open `macro_and_commodities_dashboard.pbix`.

---

## How to Refresh the Data

1. Retrieve a free **Alpha Vantage API key** from: https://www.alphavantage.co/support/#api-key
2. Open and run `macro_and_commodities_dashboard.py`.
3. Enter your API key when prompted.
4. Refresh the data in Power BI to load the updated CSV files.

---

## Notes

- Data is updated manually by running the Python script.
- CSV files are intentionally used to keep the project simple and user-friendly.
- Designed for local use (no database required).
- Data is collected at a monthly frequency.

---

