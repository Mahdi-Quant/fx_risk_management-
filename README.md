# fx_risk_management Project README

## Overview :
This project provides tools for analyzing and forecasting foreign exchange (FX) risk, with a focus on Value at Risk (VaR), Expected Shortfall (ES), and Monte Carlo simulation for exchange rate forecasting. The code is designed to help companies manage FX exposure and make informed decisions in international trade.

Project Structure
**risk_metrics.py**: Calculates static and dynamic Value at Risk (VaR) and Expected Shortfall (ES) using historical returns and GARCH modeling. Outputs results to Excel files.

**fx_forecast.py**: Performs Monte Carlo simulations to forecast future exchange rates, plots confidence intervals, and includes backtesting for model evaluation.

**transactions_forecast.py**: (If included) Simulates and visualizes future payment transactions based on historical data.

**historical_rates.xlsx**: Excel file containing historical exchange rate data (required for analysis).

**payment.xlsx**: Excel file with payment transaction data (used in transactions_forecast.py).
