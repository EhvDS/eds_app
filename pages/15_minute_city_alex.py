import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Loading the data
df_neighborhoods = pd.read_csv("./data/buurten_data_alex.csv", sep=';')

print(df_neighborhoods.head())

st.title("15 Minutes City")

st.subheader("Find the closest path from A to B")


st.dataframe(df_neighborhoods)

latitude, longitude = df_neighborhoods['geo_point_2d'].str.split(",", expand=True).astype(float)

m = folium.Map(location=[latitude, longitude], zoom_start=13)

# Add a GeoJSON layer to the map
folium.GeoJson(
    data=df_neighborhoods['geo_shape'],
    name='geojson'
).add_to(m)

# Display the map in Streamlit
folium_static(m)