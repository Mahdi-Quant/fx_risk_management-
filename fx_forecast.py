import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Load historical exchange rate data
data = pd.read_excel("historical_rates.xlsx")
data['Date'] = pd.to_datetime(data['date'])
data.set_index('Date', inplace=True)

# Calculate daily returns
returns = data['EURTND'].pct_change().dropna()

# Set the number of Monte Carlo simulations
num_simulations = 1000

# Define the target end date for the forecast
target_end_date = pd.to_datetime('2024-12-30')

# Define the number of days to forecast
trading_days = (target_end_date - data.index[-1]).days
forecast_days = trading_days

# Create an array to store the simulation results
simulation_results = np.zeros((forecast_days, num_simulations))

# Set the initial exchange rate as the last observed value
initial_exchange_rate = data['EURTND'].iloc[-1]

# Run the Monte Carlo simulation
for i in range(num_simulations):
    daily_returns = np.random.choice(returns, size=forecast_days)
    cumulative_returns = np.cumprod(1 + daily_returns)
    simulation_results[:, i] = initial_exchange_rate *cumulative_returns

# Create a DataFrame from the simulation results
simulation_df = pd.DataFrame(simulation_results,index=pd.date_range(start=data.index[-1], periods=forecast_days))
simulation_df.columns = [f'Simulation {i + 1}' for i in range(num_simulations)]

# Model Evaluation with 99% Confidence Interval
mean_forecast = simulation_df.mean(axis=1)
std_dev_forecast = simulation_df.std(axis=1)
confidence_interval_lower = mean_forecast - 2.576 * std_dev_forecast
confidence_interval_upper = mean_forecast + 2.576 * std_dev_forecast

# Plotting Mean Forecast and Confidence Interval
plt.figure(figsize=(10, 6))
plt.plot(data['EURTND'], label='Historical Data', color='blue')
plt.plot(simulation_df.index, mean_forecast, color='red', label='MeanForecast', linestyle='dashed')
plt.fill_between(simulation_df.index, confidence_interval_lower,confidence_interval_upper, color='gray', alpha=0.3, label='99%Confidence Interval')
plt.title('Monte Carlo Mean Forecast with 99% Confidence Interval')
plt.xlabel('Date')
plt.ylabel('EURTND')
plt.legend()
plt.show()

# Backtesting
backtest_start_date = data.index[-forecast_days:]
backtest_actual_values = data.loc[backtest_start_date, 'EURTND']

# Plotting Backtesting Results
plt.figure(figsize=(10, 6))
plt.plot(backtest_actual_values, label='Actual Values', color='blue')
plt.plot(mean_forecast.index, mean_forecast.values, label='MeanForecast', color='red', linestyle='dashed')
plt.fill_between(mean_forecast.index, confidence_interval_lower,confidence_interval_upper, color='gray', alpha=0.3, label='99%Confidence Interval')
plt.title('Monte Carlo Backtesting Results with 99% ConfidenceInterval')
plt.xlabel('Date')
plt.ylabel('EURTND')