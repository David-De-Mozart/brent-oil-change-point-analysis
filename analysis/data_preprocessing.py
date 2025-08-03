import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
import re
from statsmodels.tsa.stattools import adfuller

def preprocess_data():
    # Load raw data
    data_path = '../data/brent_prices.csv'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at {data_path}")
    
    # Read data without parsing dates initially
    df = pd.read_csv(data_path)
    
    # Basic data validation
    if 'Date' not in df.columns or 'Price' not in df.columns:
        raise ValueError("Data must contain 'Date' and 'Price' columns")
    
    # Custom date parser that handles multiple formats
    def parse_date(date_str):
        # Clean the string
        date_str = str(date_str).strip()
        
        # Try different formats
        formats = [
            '%d-%b-%y',    # 20-May-87
            '%b %d, %Y',   # Apr 22, 2020
            '%Y-%m-%d',    # 2020-04-22
            '%m/%d/%Y'     # 04/22/2020
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        # Handle special cases
        try:
            # Handle "May 20, 1987" format
            if re.match(r'[A-Za-z]{3} \d{1,2}, \d{4}', date_str):
                return datetime.strptime(date_str, '%b %d, %Y')
        except:
            pass
        
        # If all formats fail, return NaT
        return pd.NaT
    
    # Apply the custom parser
    df['Date'] = df['Date'].apply(parse_date)
    
    # Remove rows with invalid dates
    original_count = len(df)
    df = df.dropna(subset=['Date'])
    new_count = len(df)
    
    if original_count > new_count:
        print(f"Warning: Removed {original_count - new_count} rows with invalid dates")
    
    # Convert and sort dates
    df = df.sort_values('Date').set_index('Date')
    
    # Handle missing values in price
    print(f"Missing values before: {df['Price'].isnull().sum()}")
    df['Price'] = df['Price'].interpolate(method='time')
    print(f"Missing values after: {df['Price'].isnull().sum()}")
    
    # Handle zero/negative prices
    if (df['Price'] <= 0).any():
        print("Warning: Negative or zero prices found. Applying absolute value.")
        df['Price'] = df['Price'].abs()
    
    # Calculate log returns
    df['Log_Return'] = np.log(df['Price']) - np.log(df['Price'].shift(1))
    df = df.dropna()
    
    # Stationarity test
    def check_stationarity(series):
        result = adfuller(series.dropna())
        print(f"ADF Statistic: {result[0]:.4f}")
        print(f"p-value: {result[1]:.4f}")
        return result[1] < 0.05
    
    print("\nStationarity Tests:")
    price_stationary = check_stationarity(df['Price'])
    returns_stationary = check_stationarity(df['Log_Return'])
    
    print(f"\nPrice Stationary: {price_stationary}")
    print(f"Returns Stationary: {returns_stationary}")
    
    # Save processed data
    output_path = '../data/processed_data.csv'
    df.to_csv(output_path)
    print(f"\nProcessed data saved to {output_path}")
    
    # Generate EDA plots
    plt.figure(figsize=(14, 10))
    
    # Price plot
    plt.subplot(211)
    plt.plot(df['Price'])
    plt.title('Brent Oil Prices (1987-2022)', fontsize=14)
    plt.ylabel('Price (USD)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Returns plot
    plt.subplot(212)
    plt.plot(df['Log_Return'])
    plt.title('Daily Log Returns', fontsize=14)
    plt.ylabel('Log Return', fontsize=12)
    plt.xlabel('Date', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plot_path = '../analysis/price_and_returns.png'
    plt.savefig(plot_path)
    print(f"EDA plot saved to {plot_path}")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Data range: {df.index.min().date()} to {df.index.max().date()}")
    print(f"Number of observations: {len(df)}")
    print(f"Average price: ${df['Price'].mean():.2f}")
    print(f"Min price: ${df['Price'].min():.2f}")
    print(f"Max price: ${df['Price'].max():.2f}")
    print(f"Average daily return: {df['Log_Return'].mean():.6f}")
    print(f"Return volatility: {df['Log_Return'].std():.4f}")
    
    return df

if __name__ == '__main__':
    try:
        print("Starting data preprocessing...")
        df = preprocess_data()
        print("\nData preprocessing completed successfully!")
    except Exception as e:
        print(f"\nError in data preprocessing: {str(e)}")
        # Print traceback for debugging
        import traceback
        traceback.print_exc()