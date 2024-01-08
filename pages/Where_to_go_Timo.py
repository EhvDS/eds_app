import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Laden van de dataset
data = pd.read_csv("./data/Timo_Where_to_go.csv", sep=";")

# Unieke waarden voor filters
unique_project_fases = data['PROJECTFASE'].unique()

# Streamlit sidebar voor filters
selected_project_fase = st.sidebar.selectbox('Selecteer een projectfase', unique_project_fases)

# Filteren van de data op basis van geselecteerde projectfase
filtered_data = data[data['PROJECTFASE'] == selected_project_fase]

# Kaart van Eindhoven
m = folium.Map(location=[51.4416, 5.4697], zoom_start=12)  # Coördinaten voor Eindhoven

# Toevoegen van markers voor gefilterde data
for idx, row in filtered_data.iterrows():
    lat, lon = row['geo_point_2d'].split(',')
    folium.Marker(location=[float(lat), float(lon)], popup=row['NAAMPROJECT']).add_to(m)

# Weergeven van de kaart in Streamlit
st.header(f"Projecten in de fase: {selected_project_fase}")
st.markdown("Kaart van Eindhoven met gefilterde projecten")
folium_static(m)
