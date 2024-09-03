#Familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and
#record low temperatures by day of the year over the period 2005-2014. The area between the record high and 
#record low temperatures for each day should be shaded. 
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
temperature_df = pd.read_csv('temperature.csv')

# Convert 'Date' column to datetime
temperature_df['Date'] = pd.to_datetime(temperature_df['Date'])

# Extract year and day of year
temperature_df['year'] = temperature_df['Date'].dt.year
temperature_df['day_of_year'] = temperature_df['Date'].dt.dayofyear

# Filter data for 2005-2014
temperature_df = temperature_df[temperature_df['year'].between(2005, 2014)]

# Remove leap days
temperature_df = temperature_df[~((temperature_df['Date'].dt.month == 2) & (temperature_df['Date'].dt.day == 29))]

# Calculate record highs and lows
record_highs = temperature_df[temperature_df['Element'] == 'TMAX'].groupby('day_of_year')['Data_Value'].max()
record_lows = temperature_df[temperature_df['Element'] == 'TMIN'].groupby('day_of_year')['Data_Value'].min()

# Create the plot
plt.figure(figsize=(14, 7))
plt.plot(record_highs.index, record_highs.values, label='Record Highs', color='red')
plt.plot(record_lows.index, record_lows.values, label='Record Lows', color='blue')
plt.fill_between(record_highs.index, record_lows.values, record_highs.values, color='grey', alpha=0.3)

# Format the plot
plt.title('Record High and Low Temperatures by Day of the Year (2005-2014)')
plt.xlabel('Day of the Year')
plt.ylabel('Temperature (tenths of degrees C)')
plt.legend()
plt.grid(True)

# Save the plot to a file and display
plt.savefig('plot.png')  # Save as an image file
plt.show()  # Display the plot
