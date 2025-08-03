from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS
import os
import traceback
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def safe_read_csv(path, date_cols=None):
    try:
        print(f"Attempting to read: {path}")
        if not os.path.exists(path):
            print(f"File not found: {path}")
            return pd.DataFrame()
            
        if date_cols:
            df = pd.read_csv(path, parse_dates=date_cols)
            # Convert dates to ISO format strings
            for col in date_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
            return df
        return pd.read_csv(path)
    except Exception as e:
        print(f"Error reading {path}: {str(e)}")
        traceback.print_exc()
        return pd.DataFrame()

@app.route('/api/data')
def get_data():
    try:
        # Get the absolute path to the project root
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        print(f"Base directory: {base_dir}")
        
        # Define file paths
        data_files = {
            'prices': os.path.join(base_dir, 'data', 'processed_data.csv'),
            'impacts': os.path.join(base_dir, 'analysis', 'event_impacts.csv'),
            'change_points': os.path.join(base_dir, 'analysis', 'change_points.csv')
        }
        
        # Log file status
        for name, path in data_files.items():
            print(f"{name} path: {path}")
            print(f"{name} exists: {os.path.exists(path)}")
            print(f"{name} size: {os.path.getsize(path) if os.path.exists(path) else 0} bytes")
        
        # Load data
        prices = safe_read_csv(data_files['prices'], date_cols=['Date'])
        impacts = safe_read_csv(data_files['impacts'])
        change_points = safe_read_csv(data_files['change_points'])
        
        # Log data status
        print(f"Prices rows: {len(prices)}")
        print(f"Impacts rows: {len(impacts)}")
        print(f"Change points rows: {len(change_points)}")
        
        # Convert to dictionaries
        prices_dict = prices.to_dict('records') if not prices.empty else []
        impacts_dict = impacts.to_dict('records') if not impacts.empty else []
        change_points_dict = change_points.to_dict('records') if not change_points.empty else []
        
        # Create response
        response = {
            'prices': prices_dict,
            'events': impacts_dict,
            'changePoints': change_points_dict,
            'meta': {
                'prices_count': len(prices_dict),
                'events_count': len(impacts_dict),
                'change_points_count': len(change_points_dict),
                'generated_at': datetime.now().isoformat()
            }
        }
        
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': f"Server error: {str(e)}",
            'trace': traceback.format_exc()
        }), 500

@app.route('/api/debug')
def debug_info():
    try:
        # Get the absolute path to the project root
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        
        # List directory contents
        def list_dir(path):
            try:
                return {
                    'path': path,
                    'exists': os.path.exists(path),
                    'is_dir': os.path.isdir(path),
                    'contents': [f for f in os.listdir(path)] if os.path.exists(path) and os.path.isdir(path) else []
                }
            except Exception as e:
                return {'error': str(e)}
        
        return jsonify({
            'working_directory': os.getcwd(),
            'base_dir': base_dir,
            'data_dir': list_dir(os.path.join(base_dir, 'data')),
            'analysis_dir': list_dir(os.path.join(base_dir, 'analysis')),
            'environment': dict(os.environ)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy', 
        'version': '1.0.0',
        'time': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)