import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import folium_static


# Loading the data
df_neighborhoods = pd.read_csv("./data/buurten_data_alex.csv", sep=';')

st.title("15 Minutes City")

st.subheader("Find the closest path from A to B")

threshold = st.number_input("Enter the threshold (in minutes):", min_value=0, max_value=60, step=1, value=15)

st.dataframe(df_neighborhoods)

df_neighborhoods[['latitude', 'longitude']] = df_neighborhoods['geo_point_2d'].str.split(",", expand=True).astype(float)

# Create a map
m = folium.Map(location=[df_neighborhoods['latitude'].mean(), df_neighborhoods['longitude'].mean()], zoom_start=13)

# Add the GeoJSON data to the map
for _, row in df_neighborhoods.iterrows():
    geojson_data = json.loads(row['geo_shape'])
    folium.GeoJson(geojson_data).add_to(m)

    # Add a marker in the middle of each neighborhood
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        # Create a popup with the name and other information
        popup=folium.Popup(f"Name: {row['BUURTNAAM']}, District: {row['WIJKNAAM']}", max_width=250)
    ).add_to(m)

# Display the map in Streamlit
folium_static(m)
