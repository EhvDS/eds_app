import streamlit as st
import pandas as pd
import json
import folium
import networkx as nx
from geopy.distance import geodesic
from streamlit_folium import folium_static


# Loading the data
df_neighborhoods = pd.read_csv("./data/buurten_data_alex.csv", sep=';')

st.title("15 Minutes City")

st.subheader("Find the closest path from A to B")

# Add an input for the minutes
minutes = st.number_input("Enter the minutes:", min_value=0, max_value=60, step=1, value=15)

threshold = minutes * 4 / 60


st.dataframe(df_neighborhoods)

df_neighborhoods[['latitude', 'longitude']] = df_neighborhoods['geo_point_2d'].str.split(",", expand=True).astype(float)

# Create a graph
G = nx.Graph()

# Function to calculate distance
def calculate_distance(point1, point2):
    return geodesic(point1, point2).km

# Add nodes and edges to the graph
for index, row in df_neighborhoods.iterrows():
    for index2, row2 in df_neighborhoods.iterrows():
        if index != index2:
            distance = calculate_distance((row['latitude'], row['longitude']), (row2['latitude'], row2['longitude']))
            if distance <= threshold:  # Only add connections under threshold
                G.add_node(row['BUURTNAAM'], pos=(row['latitude'], row['longitude']))
                G.add_node(row2['BUURTNAAM'], pos=(row2['latitude'], row2['longitude']))
                G.add_edge(row['BUURTNAAM'], row2['BUURTNAAM'])

# Draw the graph
nx.draw(G, with_labels=True)
st.pyplot()

# Draw the graph
nx.draw(G, with_labels=True)
st.pyplot()


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


