import streamlit as st
import folium
from streamlit_folium import folium_static

# Data for Eindhoven map
eindhoven_coordinates = (51.4416, 5.4697)  # Coordinates for Eindhoven

# Sample data points (replace this with your actual data)
data_points = [
    {"name": "Location A", "lat": 51.4443, "lon": 5.4699},
    {"name": "Location B", "lat": 51.4388, "lon": 5.4763},
    # Add more data points as needed
]

# Create a Streamlit sidebar for filters
st.sidebar.header("Map Filters")
# Add filters here, for example:
min_distance = st.sidebar.slider("Minimum distance", min_value=0, max_value=10, value=2)

# Create the map using Folium
m = folium.Map(location=eindhoven_coordinates, zoom_start=14)

# Add markers for each data point
for point in data_points:
    folium.Marker(
        location=(point['lat'], point['lon']),
        popup=point['name']
    ).add_to(m)

# Display the map in Streamlit
st.header("Map of Eindhoven")
st.markdown("Here's a map of Eindhoven with markers.")
folium_static(m)