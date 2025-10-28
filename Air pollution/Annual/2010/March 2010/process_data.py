# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 15:16:53 2025

@author: Sneha Umbrajkar
"""

import pandas as pd

# what columns actually exist in file

df = pd.read_excel('Udyog_bhavan_data_march2010.xlsx')
print(f"File shape: {df.shape}")
print(f"Columns found: {df.columns.tolist()}")
print("\nFirst 5 rows:")
print(df.head())


expected_columns = ['Date', 'Abs.', 'V(m3)', 'Conc.', 'Aveg.']
existing_columns = []

for col in expected_columns:
    if col in df.columns:
        print(f"Found column: {col}")
        existing_columns.append(col)
    else:
        print(f" Missing column: {col}")

#  If 'Date' column exists
if 'Date' in df.columns:
   
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    
    invalid_dates = df['Date'].isna().sum()
    if invalid_dates > 0:
        print(f" {invalid_dates} rows have invalid dates and will be removed")
        df = df.dropna(subset=['Date'])
    
    df.sort_values(by='Date', inplace=True)
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    # 4. Filter by date
    start_date = '2010-03-01' 
    filtered_df = df[df['Date'] >= start_date]
    print(f"After filtering: {filtered_df.shape[0]} rows")
    
    # 5. Select only existing columns
    final_columns = [col for col in existing_columns if col in filtered_df.columns]
    final_df = filtered_df[final_columns]
    
    # 6. Save to CSV
    final_df.to_csv('filtered_sorted_data.csv', index=False)
    print("\n File saved successfully !")
    print(f"Final data shape: {final_df.shape}")
    print("\nFirst 5 rows of final data:")
    print(final_df.head())
    
else:
    print("\n No 'Date' column found ")
    
    # Save the raw data for analysis
    df.to_csv('raw_data_analysis.csv', index=False)
    print("Raw data saved as 'raw_data_analysis.csv'")
    
    #data pre processing
    
station_1_data = pd.read_csv('filtered_sorted_data.csv')
import matplotlib.pyplot as plt
#station_1_data = daily_data[daily_data['Station'] == 'Udyoga Bhawan']
plt.figure(figsize=(12,5))
plt.plot(station_1_data['Date'], station_1_data['Aveg.'])
plt.title('NOx Levels over Time - Udyoga Bhawan')
plt.xlabel('Date'); plt.ylabel('NOx Concentration')
plt.show()
    