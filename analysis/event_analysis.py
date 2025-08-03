import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

def analyze_event_impacts():
    print("\nAnalyzing event impacts...")
    
    try:
        # Load data
        data_path = BASE_DIR.parent / 'data' / 'processed_data.csv'
        df = pd.read_csv(data_path, parse_dates=['Date'], index_col='Date')
        df = df.loc['2012-01-01':'2022-09-30']
        
        # Load change points
        cp_path = BASE_DIR / 'change_points.csv'
        change_points = pd.read_csv(cp_path, parse_dates=['Change_Point'])
        
        # Load events
        events_path = BASE_DIR.parent / 'data' / 'events.csv'
        events = pd.read_csv(events_path, parse_dates=['Date'])
        
        # Analyze each change point
        results = []
        for cp in change_points['Change_Point']:
            # Find closest event within 30 days
            time_diff = (events['Date'] - cp).abs()
            closest_idx = time_diff.idxmin()
            closest_event = events.loc[closest_idx]
            days_diff = time_diff.min().days
            
            if days_diff <= 30:
                # Calculate price impact
                window = 30
                pre = df[cp - pd.Timedelta(days=window):cp]['Price'].mean()
                post = df[cp:cp + pd.Timedelta(days=window)]['Price'].mean()
                pct_change = (post - pre) / pre * 100
                
                # Calculate volatility impact
                pre_vol = df[cp - pd.Timedelta(days=window):cp]['Log_Return'].std()
                post_vol = df[cp:cp + pd.Timedelta(days=window)]['Log_Return'].std()
                vol_pct_change = (post_vol - pre_vol) / pre_vol * 100
                
                results.append({
                    'Change_Point': cp,
                    'Event': closest_event['Event'],
                    'Event_Date': closest_event['Date'],
                    'Days_Diff': days_diff,
                    'Price_Change_Pct': pct_change,
                    'Volatility_Change_Pct': vol_pct_change
                })
        
        # Save results
        results_path = BASE_DIR / 'event_impacts.csv'
        pd.DataFrame(results).to_csv(results_path, index=False)
        print(f"Event impacts saved to {results_path}")
        
        return results
        
    except Exception as e:
        print("Error:", e)
        return []

if __name__ == '__main__':
    results = analyze_event_impacts()
    print("\nEvent Impact Analysis Results:")
    for r in results:
        print(f"\nEvent: {r['Event']} ({r['Event_Date'].strftime('%Y-%m-%d')})")
        print(f"Detected Change Point: {r['Change_Point'].strftime('%Y-%m-%d')} ({r['Days_Diff']} days after event)")
        print(f"Price Change: {r['Price_Change_Pct']:.2f}%")
        print(f"Volatility Change: {r['Volatility_Change_Pct']:.2f}%")