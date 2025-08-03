import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az
import pytensor.tensor as pt
import time
from pathlib import Path

# Get the absolute path to the script's directory
BASE_DIR = Path(__file__).parent.resolve()

def detect_change_points():
    print("\nStarting optimized change point detection...")
    start_time = time.time()
    
    try:
        # Load data with absolute path
        data_path = BASE_DIR.parent / 'data' / 'processed_data.csv'
        print(f"Loading data from: {data_path}")
        df = pd.read_csv(data_path, parse_dates=['Date'], index_col='Date')
        
        # Filter to last decade (2012-2022)
        df = df.loc['2012-01-01':'2022-09-30']
        returns = df['Log_Return'].values
        dates = df.index
        n = len(returns)
        print(f"Analyzing {n} days of returns (2012-2022)")
        
        with pm.Model() as model:
            # Prior for change point location
            tau = pm.DiscreteUniform("tau", lower=0, upper=n-1)
            
            # Priors for mean and volatility
            mu1 = pm.Normal("mu1", mu=0, sigma=0.1)
            mu2 = pm.Normal("mu2", mu=0, sigma=0.1)
            sigma = pm.HalfNormal("sigma", sigma=0.1)
            
            # Vectorized mean calculation using PyTensor
            idx = pt.arange(n)
            mu = pt.switch(idx < tau, mu1, mu2)
            
            # Likelihood
            obs = pm.Normal("obs", mu=mu, sigma=sigma, observed=returns)
            
            # Fast sampling with reduced tuning
            print("Running optimized MCMC sampling...")
            step = pm.Metropolis(vars=[tau])  # Metropolis for discrete variable
            trace = pm.sample(
                6000,  # Reduced samples
                tune=1000,  # Reduced tuning
                chains=2,
                step=[step, pm.NUTS([mu1, mu2, sigma])],  # Hybrid sampler
                cores=2,  # Use 2 CPU cores
                progressbar=True,
                random_seed=42,
                return_inferencedata=True
            )
            print(f"Sampling completed in {time.time() - start_time:.1f} seconds")

        # Diagnostics
        print("\nModel Diagnostics:")
        print(az.summary(trace))
        
        # Plot trace
        az.plot_trace(trace, var_names=["mu1", "mu2", "sigma", "tau"])
        plt_path = BASE_DIR / 'trace_plot.png'
        plt.tight_layout()
        plt.savefig(plt_path)
        print(f"Trace plot saved to {plt_path}")
        
        # Extract change points
        tau_samples = trace.posterior["tau"].values.flatten()
        change_dates = pd.Series([dates[i] for i in tau_samples])
        top_change_points = change_dates.value_counts().head(3).index
        
        # Save results
        results_path = BASE_DIR / 'change_points.csv'
        pd.DataFrame({'Change_Point': top_change_points}).to_csv(results_path, index=False)
        print(f"Results saved to {results_path}")
        
        print("\nTop Change Points:")
        print(top_change_points)
        
        return top_change_points

    except Exception as e:
        print("Error:", e)
        # Fallback to fast statistical method
        print("Using fast statistical method as fallback...")
        return fallback_change_point_detection(df)

def fallback_change_point_detection(df):
    """Fallback method using rolling statistics"""
    try:
        # Calculate rolling statistics
        window = 30
        rolling_mean = df['Price'].rolling(window).mean()
        
        # Find significant changes
        price_diff = rolling_mean.diff().abs()
        top_indices = price_diff.nlargest(5).index
        
        # Save results
        results_path = BASE_DIR / 'change_points.csv'
        pd.DataFrame({'Change_Point': top_indices}).to_csv(results_path, index=False)
        
        print("\nTop Change Points (fallback method):")
        print(top_indices)
        
        return top_indices
    except:
        return []

if __name__ == '__main__':
    detect_change_points()