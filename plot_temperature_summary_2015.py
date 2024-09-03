# Plot Temperature Summary near Ann Arbor, Michigan, United States (Year 2015).
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
temperature_df = pd.read_csv('temperature.csv')

# Convert 'Date' column to datetime
temperature_df['Date'] = pd.to_datetime(temperature_df['Date'])

# Filter for the year 2015
temperature_df_2015 = temperature_df[temperature_df['Date'].dt.year == 2015]

# Add 'DayOfYear' column
temperature_df_2015['DayOfYear'] = temperature_df_2015['Date'].dt.dayofyear

# Get temperature extremes by day of the year
daily_temps = temperature_df_2015.groupby(['DayOfYear', 'Element'])['Data_Value'].agg(['min', 'max']).reset_index()

# Pivot table to get separate columns for TMAX and TMIN
pivoted_temps = daily_temps.pivot(index='DayOfYear', columns='Element', values=['min', 'max'])

# Compute daily temperature range
pivoted_temps['Range'] = pivoted_temps['max']['TMAX'] - pivoted_temps['min']['TMIN']

# Plotting
plt.figure(figsize=(14, 8))

# Plot Daily High Temperatures
plt.plot(pivoted_temps.index, pivoted_temps['max']['TMAX'], label='Daily High Temperature (TMAX)', color='red')

# Plot Daily Low Temperatures
plt.plot(pivoted_temps.index, pivoted_temps['min']['TMIN'], label='Daily Low Temperature (TMIN)', color='blue')

# Plot Daily Temperature Range
plt.plot(pivoted_temps.index, pivoted_temps['Range'], label='Daily Temperature Range', color='green')

# Adding labels and title
plt.xlabel('Day of the Year')
plt.ylabel('Temperature (Tenths of Degrees C)')
plt.title('Daily Temperature Summary for Ann Arbor, Michigan (2015)')
plt.legend()
plt.grid(True)

# Save and show the plot
plt.savefig('temperature_summary_2015.png')
plt.show()
