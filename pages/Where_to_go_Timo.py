import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Laden van de dataset
data = pd.read_csv("./data/Timo_Where_to_go.csv", sep=";")  # Vervang "bestandsnaam.csv" door de werkelijke bestandsnaam en locatie

# Unieke naamprojecten
unique_projects = data['NAAMPROJECT'].unique()

# Streamlit sidebar voor filters
selected_project = st.sidebar.selectbox('Selecteer een naamproject', unique_projects)

# Filteren van de data op basis van geselecteerd naamproject
filtered_data = data[data['NAAMPROJECT'] == selected_project]

# Kaart van Eindhoven
m = folium.Map(location=[51.4416, 5.4697], zoom_start=12)  # Coördinaten voor Eindhoven

# Groeperen van data per uniek naamproject
grouped_data = data.groupby('NAAMPROJECT')

# Marker toevoegen voor elk uniek naamproject
for name, group in grouped_data:
    locations = eval(group.iloc[0]['geo_shape'])['coordinates'][0]
    folium.GeoJson({
        "type": "Polygon",
        "coordinates": [locations]
    },
    tooltip=name,
    style_function=lambda feature: {
        'fillColor': 'red',
        'color': 'red',
        'weight': 2,
        'fillOpacity': 0.5,
    },
    popup=f"<b>{name}</b><br>{group['PROJECTFASE'].tolist()}").add_to(m)

# Weergeven van de kaart in Streamlit
st.header(f"Gekleurde gebieden voor project: {selected_project}")
st.markdown("Kaart van Eindhoven met roodgekleurde gebieden per project")
folium_static(m)
