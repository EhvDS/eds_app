import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

data = pd.read_csv('./data/Timo_Where_to_go.csv', sep=';')

# Kaart van Eindhoven initialiseren
m = folium.Map(location=[51.4416, 5.4697], zoom_start=12)

# Voeg een selectiebox toe om projectfasen te filteren
selected_phase = st.sidebar.selectbox('Selecteer projectfase', data['PROJECTFASE'].unique())

# Filter de dataset op basis van geselecteerde fase
filtered_data = data[data['PROJECTFASE'] == selected_phase]

# Itereren over de dataset om gebieden toe te voegen als rode polygoon op de kaart
for index, row in data.iterrows():
    coordinates = row['geo_shape']['coordinates']  # Coördinaten voor de polygoon van elk project

    # Polygoon toevoegen aan de kaart als een rode zone met projectnaam als popup
    folium.Polygon(
        locations=coordinates,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=1,
        popup=row['NAAMPROJECT']
    ).add_to(m)

# Weergeven van de kaart in Streamlit
st.header("Kaart van Eindhoven met rode gebieden voor elk project")
st.markdown("Elk gebied vertegenwoordigt een naamproject in de dataset.")
folium_static(m)
