import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Laden van de dataset
data = pd.read_csv("./data/Timo_Where_to_go.csv", sep=";")  # Vervang "bestandsnaam.csv" door de werkelijke bestandsnaam en locatie

# Streamlit sidebar voor filters
selected_project_fase = st.sidebar.multiselect('Project Fase', data['PROJECTFASE'].unique())
selected_building_plan = st.sidebar.multiselect('Bouwplan', data['BOUWPLAN'].unique())
selected_housing_type = st.sidebar.multiselect('Woningtype', data['WONINGTYPE'].unique())

# Filteren van de data op basis van geselecteerde filters
filtered_data = data[
    (data['PROJECTFASE'].isin(selected_project_fase)) &
    (data['BOUWPLAN'].isin(selected_building_plan)) &
    (data['WONINGTYPE'].isin(selected_housing_type))
]

# Kaart van Eindhoven
m = folium.Map(location=[51.4416, 5.4697], zoom_start=12, tiles='Stamen Terrain', control_scale=True)

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
        'fillColor': 'red' if name in filtered_data['NAAMPROJECT'].unique() else 'gray',
        'color': 'red' if name in filtered_data['NAAMPROJECT'].unique() else 'gray',
        'weight': 2,
        'fillOpacity': 0.5,
    },
    popup=f"<b>{name}</b><br>{group['PROJECTFASE'].tolist()}").add_to(m)

st.write(filtered_data)

# Weergeven van de kaart in Streamlit
st.header("Gekleurde gebieden per project")
st.markdown("Kaart van Eindhoven met gekleurde gebieden per project")
folium_static(m)
