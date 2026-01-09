from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.commodities import Commodities
from alpha_vantage.econindicators import EconIndicators
import pandas as pd
import datetime
import time
import tkinter as tk
from tkinter import simpledialog
from pathlib import Path

root = tk.Tk()
root.withdraw()
API_alpha = simpledialog.askstring("Alpha Vantage API", "Please enter your Alpha Vantage API code for fresh data:")

ts = TimeSeries(key = API_alpha, output_format='pandas')
cmd = Commodities(key = API_alpha, output_format='pandas')
ei = EconIndicators(key = API_alpha, output_format='pandas')


#%% Date Range


today = datetime.date.today()
start_date = today - datetime.timedelta(days=365*30) 
date_range = pd.date_range(start = start_date, end = today, freq='M')
date_df = pd.DataFrame({'date':date_range})


#%% Table 1


macro_list = {'Inflation':'cpi', 'Interest':'ffr','Unemployment':'unemployment', 'GDP':'real_gdp'}           
macro_data = []

for name, symbol in macro_list.items():
    data, meta = getattr(ei, f"get_{symbol}")()
    data = data.reset_index(drop=True)
    data['date'] = (pd.to_datetime(data['date']) - pd.offsets.MonthEnd(1))
    temp_df = pd.DataFrame({'date':data['date'], 'value':data['value'], 'indicator':name})
    macro_data.append(temp_df)
    time.sleep(15)

for symbol in ['SPY']:
    sp500_data, meta = ts.get_monthly_adjusted(symbol=symbol)
    sp500_data = sp500_data.reset_index()
    sp500_df = pd.DataFrame()    
    sp500_df['date'] = (pd.to_datetime(sp500_data['date']) - pd.offsets.MonthEnd(0))
    sp500_df['value'] = (sp500_data['5. adjusted close'])
    sp500_df['indicator'] = 'S&P 500'
    time.sleep(15)

macro_data.append(sp500_df)
macro_df = pd.concat(macro_data, ignore_index=True)
macro_df['value'] = pd.to_numeric(macro_df['value'], errors="coerce")
macro_df = macro_df.sort_values('date')

macro_unique = pd.DataFrame({'indicator': macro_df['indicator'].unique()})
full_index_macro = (date_df.assign(key=1).merge(macro_unique.assign(key=1), on='key').drop('key', axis=1))
macro_merged = full_index_macro.merge(macro_df, on=['date','indicator'], how='left')

macro_unit_map = {'Inflation':'Index', 'Interest':'Percent','Unemployment':'Percent',
                  'GDP':'Billions of Dollars', 'S&P 500':'Adjusted Close (SPY)'}  

macro_merged['unit'] = macro_merged['indicator'].map(macro_unit_map)
macro_df = macro_merged.copy()
        
                            
#%% Table 2


commodities_list = {'Oil':'brent', 'Gas':'natural_gas',
                    'Copper':'copper', 'Aluminum':'aluminum',
                    'Wheat':'wheat', 'Corn':'corn', 'Cotton':'cotton', 
                    'Sugar':'sugar', 'Coffee':'coffee'}
commodities_data = []

for name, symbol in commodities_list.items():
    data, meta = getattr(cmd, f"get_{symbol}")()
    data = data.reset_index(drop=True)
    data['date'] = (pd.to_datetime(data['date']) - pd.offsets.MonthEnd(1))
    temp_df = pd.DataFrame({'date':data['date'], 'price':data['value'], 'commodity':name})
    commodities_data.append(temp_df)
    time.sleep(15)

for symbol in ['GLD']:
    gold_data, meta = ts.get_monthly(symbol=symbol)
    gold_data = gold_data.reset_index()
    gold_df = pd.DataFrame()
    gold_df['date'] = (pd.to_datetime(gold_data['date']) - pd.offsets.MonthEnd(0))
    gold_df['price'] = (gold_data['4. close'])
    gold_df['commodity'] = 'Gold'
    time.sleep(15)
    
commodities_data.append(gold_df)
commodities_df = pd.concat(commodities_data, ignore_index=True)
commodities_df['price'] = pd.to_numeric(commodities_df['price'], errors="coerce")
commodities_df = commodities_df.sort_values('date')

commodity_unique = pd.DataFrame({'commodity': commodities_df['commodity'].unique()})
full_index_commodity = (date_df.assign(key=1).merge(commodity_unique.assign(key=1), on='key').drop('key', axis=1))
commodities_merged = full_index_commodity.merge(commodities_df, on=['date','commodity'], how='left')

category_map = {'Oil':'Energy', 'Gas':'Energy',
                    'Copper':'Industrial Metal', 'Aluminum':'Industrial Metal',
                    'Wheat':'Agriculture', 'Corn':'Agriculture', 'Cotton':'Agriculture', 
                    'Sugar':'Agriculture', 'Coffee':'Agriculture', 'Gold': 'Precious Metals'}
commodities_merged['category'] = commodities_merged['commodity'].map(category_map)

commodities_unit_map = {'Oil':'Dollars per Barrel', 'Gas':'Dollars per Million BTU',
                        'Copper':'U.S. Dollars per Metric Ton', 'Aluminum':'U.S. Dollars per Metric Ton',
                        'Wheat':'U.S. Dollars per Metric Ton', 'Corn':'U.S. Dollars per Metric Ton', 'Cotton':'U.S. Cents per Pound', 
                        'Sugar':'U.S. Cents per Pound', 'Coffee':'U.S. Cents per Pound', 'Gold': 'USD / Share (GLD ETF)'}
commodities_merged['unit'] = commodities_merged['commodity'].map(commodities_unit_map)
commodities_df = commodities_merged.copy()


#%% Export Data


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

macro_df.to_csv(DATA_DIR / "macro_data.csv", index=False)
commodities_df.to_csv(DATA_DIR / "commodities_data.csv", index=False)
print("Data saved to ./data/")

