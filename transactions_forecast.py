import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Load payment data from an Excel file, ensuring chronologicalorder.
def load_payment_data(file_path):
    data = pd.read_excel(file_path)
    data['date'] = pd.to_datetime(data['date'])
    return data.sort_values(by='date')
#Compute the distribution of intervals between consecutive payments.
def compute_payment_intervals(data):
    intervals = data['date'].diff().dt.days
    return intervals[intervals > 0].value_counts().sort_index()

#Simulate future payments over a given period.
def simulate_future_payments(payment_data, months_to_simulate,simulation_count):

    last_payment_date = payment_data['date'].iloc[-1]
    interval_dist = compute_payment_intervals(payment_data)
    intervals = interval_dist.index.to_numpy()
    probabilities = interval_dist.values / interval_dist.values.sum()
    future_payments = []
    for _ in range(months_to_simulate * 30):
        interval = np.random.choice(intervals, p=probabilities)
        date = last_payment_date + pd.Timedelta(days=interval)
        amount = np.random.choice(payment_data['Montant'], size=simulation_count).mean()  
        future_payments.append([date, amount])
        last_payment_date = date # Update last payment date
    return pd.DataFrame(future_payments, columns=['date','average_amount'])

#Plot simulation results of future payments.
def display_simulation_plot(simulated_data):

    plt.figure(figsize=(10, 5))
    plt.plot(simulated_data['date'], simulated_data['average_amount'],
    marker='o', linestyle='-', color='blue')
    plt.title('Simulated Future Payments')
    plt.xlabel('Date')
    plt.ylabel('Average Payment Amount')
    plt.grid(True)
    plt.show()

# File path to your Excel file
file_path = 'payment.xlsx'

# Load data
payment_data = load_payment_data(file_path)

# Simulate future payments for 6 months with 1000 simulations each
simulated_payments = simulate_future_payments(payment_data, 6, 1000)

# Plot the results
display_simulation_plot(simulated_payments)

# Export the simulated data to an Excel file
output_file_path = 'simulated_future_transactions.xlsx' # Set the output file name
simulated_payments.to_excel(output_file_path, index=False)
print("excel exported successfully")