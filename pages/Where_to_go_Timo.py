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

# Function to update the map with filtered data
def update_map(filtered_data):
    m = folium.Map(location=[51.45129, 5.45475], zoom_start=12)
    for index, row in filtered_data.iterrows():
        phase = row['PROJECTFASE']
        color = color_dict.get(phase, 'red')  # Default color if not found in color_dict
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['naamproject'],
            icon=folium.Icon(color=color)
        ).add_to(m)
    return m

# Define a color dictionary based on filters
color_dict = {
    'PROJECTFASE_1': 'blue',  # Define colors based on PROJECTFASE values
    'PROJECTFASE_2': 'green',
}
# Display the initial map
folium_static(m)

# Display the map in Streamlit
st.header("Map of Eindhoven with Filtered Data")
st.markdown("Map showing filtered housing projects in Eindhoven.")

# Update map when filters change
if filtered_data.shape[0] > 0:
    updated_map = update_map(filtered_data)
    folium_static(updated_map)
else:
    st.warning("No data available with selected filters.")