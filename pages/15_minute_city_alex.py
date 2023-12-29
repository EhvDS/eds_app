import streamlit as st
import pandas as pd
import json
import folium
from geopy.distance import geodesic
from streamlit_folium import folium_static


# Loading the data
df_neighborhoods = pd.read_csv("./data/buurten_data_alex.csv", sep=';')
df_neighborhoods[['latitude', 'longitude']] = df_neighborhoods['geo_point_2d'].str.split(",", expand=True).astype(float)

st.title("15 Minutes City")
st.subheader("Visualize and understand the connectivity between neighborhoods within a specified walking or biking time")

# Add an input for the minutes
minutes = st.number_input("Enter the minutes:", min_value=0, max_value=60, step=1, value=15)
threshold = minutes * 4 / 60 # Assuming the average walking speed is 4 km per hour

# Function to calculate distance
def calculate_distance(point1, point2):
    return geodesic(point1, point2).km

# Create a map using folium
m = folium.Map(location=[df_neighborhoods['latitude'].mean(), df_neighborhoods['longitude'].mean()], zoom_start=13)

# Add the GeoJSON data to the map and markers only for neighborhoods within the threshold
for index, row in df_neighborhoods.iterrows():
    for index2, row2 in df_neighborhoods.iterrows():
        if index != index2:
            distance = calculate_distance((row['latitude'], row['longitude']), (row2['latitude'], row2['longitude']))
            if distance <= threshold:  # Only add connections under threshold
                geojson_data = json.loads(row['geo_shape'])
                folium.GeoJson(geojson_data).add_to(m)
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    radius=0.2,
                    # Create a popup with the name and other information
                    popup=folium.Popup(f"Name: {row['BUURTNAAM']}, District: {row['WIJKNAAM']}", max_width=250)
                ).add_to(m)
                folium.PolyLine([(row['latitude'], row['longitude']), (row2['latitude'], row2['longitude'])], color="blue", weight=2.5, opacity=1).add_to(m)

# Display the map in Streamlit
folium_static(m)

