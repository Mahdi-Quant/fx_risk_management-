import pandas as pd
import numpy as np
from arch import arch_model
from scipy.stats import norm

# Load the Excel file
file_path = "historical_rates.xlsx" 
df = pd.read_excel(file_path)

# Extracting the returns from the dataframe
returns = df['daily returns']

# Function to calculate static Value at Risk (VaR)
def static_var(returns, alpha=0.05):
    return np.percentile(returns, alpha * 100)

# Function to calculate Expected Shortfall (ES)
def expected_shortfall(returns, alpha=0.05):
    var = static_var(returns, alpha)
    return returns[returns < -var].mean()

# Calculating static VaR and Expected Shortfall for alpha 1% and 5%
static_var_1 = static_var(returns, alpha=0.01)
static_es_1 = expected_shortfall(returns, alpha=0.01)
static_var_5 = static_var(returns, alpha=0.05)
static_es_5 = expected_shortfall(returns, alpha=0.05)

# Fit a GARCH(1,1) model to the daily returns
model = arch_model(returns, vol='Garch', p=1, q=1)
model_fit = model.fit(disp='off')

# Forecast future volatility
forecasts = model_fit.forecast(horizon=1, start=0)

# Calculate dynamic VaR using the forecasts
z_score_1 = norm.ppf(1 - 0.01)
z_score_5 = norm.ppf(1 - 0.05)
dynamic_var_1 = -forecasts.mean['h.1'] - z_score_1 * np.sqrt(forecasts.variance['h.1'])
dynamic_var_5 = -forecasts.mean['h.1'] - z_score_5 * np.sqrt(forecasts.variance['h.1'])

# Creating a DataFrame to store the dynamic VaR results
dynamic_results = pd.DataFrame({
    'Date': df['date'],
    'Dynamic VaR 1%': dynamic_var_1,
    'Dynamic VaR 5%': dynamic_var_5
})

# Creating a dictionary to store the static VaR and ES values
static_results = {
    'Static VaR 1%': static_var_1,
    'Static ES 1%': static_es_1,
    'Static VaR 5%': static_var_5,
    'Static ES 5%': static_es_5
}

# Write the results to an Excel file
output_file_path = "D:\\SENIOR\\FRM\\Project\\VaR_ES_results.xlsx"
with pd.ExcelWriter(output_file_path) as writer:
    dynamic_results.to_excel(writer, sheet_name='Dynamic VaR',index=False)
    pd.DataFrame([static_results]).to_excel(writer, sheet_name='StaticVaR and ES', index=False)
print("Results have been saved to:", output_file_path)