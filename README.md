# Brent Oil Price Change Point Analysis

This project analyzes structural breaks in Brent crude oil prices from 1987-2022 using Bayesian change point detection. It identifies how geopolitical events impact oil markets and provides actionable insights for investors, policymakers, and energy companies.


# Key Features

- **Bayesian Change Point Detection**: Identifies structural breaks in oil prices using PyMC

- **Event Impact Analysis**: Quantifies price and volatility impacts of geopolitical events

- **Interactive Dashboard**: Visualize historical trends with event markers and change points

- **Business Intelligence**: Strategic recommendations for different stakeholders

- **Statistical Modeling**: Implements Bayesian inference with MCMC sampling


# Technologies Used

**Backend**
    - Python 3.9
    - Flask
    - PyMC
    - Pandas
    - NumPy

**Frontend**
    - React.js
    - Recharts
    - HTML/CSS
    - Axios

**Data Analysis**
    - Bayesian statistics
    - Time series analysis
    - Change point detection
    - Volatility modeling


# Installation Guide

**Prerequisites**
    - Python 3.9+
    - Node.js 16+
    - Git


# Setup Instructions

1. Clone the repository

    git clone https://github.com/dawit-senaber/brent-oil-change-point-analysis.git
    cd brent-oil-change-point-analysis

2. Set up Python environment

    - python -m venv oil_venv
    - source oil_venv/bin/activate  # Linux/Mac
    - oil_venv\Scripts\activate    # Windows
    - pip install -r requirements.txt

3. Run data analysis pipeline
    - cd analysis
    - python data_preprocessing.py
    - python change_point_model.py
    - python event_analysis.py

4. Set up and run backend
    - cd dashboard/backend
    - pip install -r requirements.txt
    - python app.py

5. Set up and run frontend
    - cd dashboard/frontend
    - npm install
    - npm start


# Project Structure

brent-oil-change-point-analysis/
├── analysis/               # Data processing and modeling scripts
│   ├── data_preprocessing.py
│   ├── change_point_model.py
│   ├── event_analysis.py
├── dashboard/              # Visualization application
│   ├── backend/            # Flask API
│   └── frontend/           # React dashboard
├── data/                   # Datasets
│   ├── raw/                # Original data files
│   └── processed/          # Processed data for analysis
├── report/model_outputs    # model_outputs
├── LICENSE
└── README.md


# Usage Guide
1. Access the Dashboard
    - Open your browser to: http://localhost:3000

2. Explore Features
    - Price Analysis: View historical prices with change points
    - Volatility Analysis: Examine market fluctuations
    - Event Impacts: Quantify effects of specific events
    - Time Filters: Adjust date ranges (1Y, 5Y, 10Y, All)

3. Interpret Results
    - Red dashed lines: Change points
    - Green lines: Geopolitical events
    - Impact cards: Price and volatility changes

4. Generate Reports
    - Export visualizations as PNG
    - Download event impact data as CSV

# Key Insights

1. Geopolitical conflicts cause 23.7% average price surges

2. OPEC decisions show effects within 7-10 days

3. COVID-19 pandemic caused largest single-day drop (-36.6%)

4. Russia-Ukraine conflict triggered $22.30/barrel price spike

5. Market stabilization occurs 15-20 days after major events


# Business Applications

**For Investors**
    - Event-driven hedging strategies
    - Volatility arbitrage opportunities
    - Regime-based portfolio allocation

**For Policymakers**
    - Strategic reserve release timing
    - Subsidy activation thresholds
    - Import diversification targets

**For Energy Companies**
    - Supply chain risk mitigation
    - Contract renegotiation windows
    - Refinery output optimization



# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Acknowledgments

- Bayesian Methods for Hackers (PyMC inspiration)
- Recharts documentation
- World Bank Commodity Price Data
- OPEC Annual Statistical Bulletin

# Contact
Email: dsenaber@gmail.com
Report Issues: GitHub Issues
