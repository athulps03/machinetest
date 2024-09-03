import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
temperature_df = pd.read_csv('temperature.csv')

# Convert 'Date' column to datetime, specifying the correct format
temperature_df['Date'] = pd.to_datetime(temperature_df['Date'], format='%d-%m-%Y')

# Extract year, month, and day of year
temperature_df['Year'] = temperature_df['Date'].dt.year
temperature_df['Month'] = temperature_df['Date'].dt.month
temperature_df['Day'] = temperature_df['Date'].dt.day
temperature_df['Day_of_Year'] = temperature_df['Date'].dt.dayofyear

# Remove leap days (February 29th)
temperature_df = temperature_df[~((temperature_df['Month'] == 2) & (temperature_df['Day'] == 29))]

# Filter data for 2005-2014
data_2005_2014 = temperature_df[(temperature_df['Year'] >= 2005) & (temperature_df['Year'] <= 2014)]

# Compute record highs and lows
record_highs = data_2005_2014[data_2005_2014['Element'] == 'TMAX'].groupby('Day_of_Year')['Data_Value'].max()
record_lows = data_2005_2014[data_2005_2014['Element'] == 'TMIN'].groupby('Day_of_Year')['Data_Value'].min()

# Filter data for 2015
data_2015 = temperature_df[temperature_df['Year'] == 2015]

# Find broken records in 2015
record_highs_series = pd.Series(record_highs, name='Record_Highs')
record_lows_series = pd.Series(record_lows, name='Record_Lows')

broken_highs = data_2015[(data_2015['Element'] == 'TMAX') & (data_2015['Data_Value'] > data_2015['Day_of_Year'].map(record_highs_series))]
broken_lows = data_2015[(data_2015['Element'] == 'TMIN') & (data_2015['Data_Value'] < data_2015['Day_of_Year'].map(record_lows_series))]

# Create the plot
plt.figure(figsize=(12, 6))

# Plot record highs and lows
plt.plot(record_highs.index, record_highs.values, label='Record Highs', color='red', linestyle='-', linewidth=2)
plt.plot(record_lows.index, record_lows.values, label='Record Lows', color='blue', linestyle='-', linewidth=2)
plt.fill_between(record_highs.index, record_lows.values, record_highs.values, color='grey', alpha=0.3)

# Overlay scatter plots for broken records in 2015
plt.scatter(broken_highs['Day_of_Year'], broken_highs['Data_Value'], color='darkred', label='2015 Highs Broken', zorder=5, marker='o', s=50)
plt.scatter(broken_lows['Day_of_Year'], broken_lows['Data_Value'], color='darkblue', label='2015 Lows Broken', zorder=5, marker='o', s=50)

# Format the plot
plt.title('Record High and Low Temperatures by Day of Year (2005-2014) Excluding Leap Days with 2015 Records Broken', fontsize=14)
plt.xlabel('Day of Year', fontsize=12)
plt.ylabel('Temperature (tenths of degrees C)', fontsize=12)
plt.legend(loc='upper left', fontsize=10)  # Place legend in the upper left with specified fontsize
plt.grid(True, linestyle='--', alpha=0.7)  # Use dashed grid lines with reduced opacity

# Remove chart junk
plt.gca().spines['top'].set_visible(False)  # Remove the top spine
plt.gca().spines['right'].set_visible(False)  # Remove the right spine
plt.gca().spines['left'].set_color('black')  # Keep left spine visible
plt.gca().spines['bottom'].set_color('black')  # Keep bottom spine visible

# Save the plot to a file
plt.savefig('plot_cleaned_visualization.png', bbox_inches='tight')  # Save as an image file with tight bounding box
plt.show()  # Display the plot
