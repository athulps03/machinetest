#Consider issues such as legends, labels, and chart junk. 
import pandas as pd
import folium

# Load the station data
stations_df = pd.read_csv('BinSize.csv')

# Filter for the relevant data near Ann Arbor, MI
ann_arbor_lat = 42.2808
ann_arbor_lon = -83.7430

# Create a base map centered around Ann Arbor
m = folium.Map(location=[ann_arbor_lat, ann_arbor_lon], zoom_start=12)

# Add markers for each station
for _, row in stations_df.iterrows():
    folium.Marker(
        location=[row['LATITUDE'], row['LONGITUDE']],  # Use correct column names for latitude and longitude
        popup=row['NAME']  # Use appropriate column for station name
    ).add_to(m)

# Save the map to an HTML file
m.save('stations_near_ann_arbor.html')

print("Map has been saved to 'stations_near_ann_arbor.html'.")
