import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static

# Data for Eindhoven map
eindhoven_coordinates = (51.4416, 5.4697)  # Coordinates for Eindhoven

# Replace 'path_to_your_dataset.csv' with your actual dataset
data = pd.read_csv("./data/Timo_Where_to_go.csv", sep=';')

# Create a Streamlit sidebar for filters
st.sidebar.header("Map Filters")

# Add filters here, for example:
selected_project_phase = st.sidebar.multiselect('Project Phase', data['PROJECTFASE'].unique())
selected_name_area = st.sidebar.multiselect('Name Area', data['NAAMDEELGEBIED'].unique())
selected_type = st.sidebar.multiselect('Type', data['WONINGTYPE'].unique())

# Filter the data based on selected filters
filtered_data = data[
    (data['PROJECTFASE'].isin(selected_project_phase)) &
    (data['NAAMDEELGEBIED'].isin(selected_name_area)) &
    (data['WONINGTYPE'].isin(selected_type))
]

# Display the filtered data
st.write(filtered_data)

# Map creation using Folium
m = folium.Map(location=[51.45129, 5.45475], zoom_start=12)

# Toevoegen van markers op de kaart gebaseerd op gefilterde data
for index, row in filtered_data.iterrows():
    folium.Marker(
        location=[row['geo_point_2d'].split(',')[0], row['geo_point_2d'].split(',')[1]],
        popup=row['NAAMPROJECT']
    ).add_to(m)


# Display the initial map
folium_static(m)

# Display the first few rows of the loaded data
print(data.head())
