import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from streamlit_folium import st_folium
import folium

# Constants
APP_TITLE = 'Eindhoven by night'
APP_SUB_TITLE = 'Data Source: [Eindhoven Public Data](https://data.eindhoven.nl/explore/dataset/data-openbare-verlichting/information/)' 

# Functions

## Options
### TODO! (if there is time)

## Plots
### Folium Map
def interactive_folium_map(df):
    # Create Map    
    map = folium.Map(
        location=[df['Latitude'].mean(), df['Longitude'].mean()], 
        tiles='cartodbdark_matter', 
        zoom_start=12
    )
    # Draw Points
    df.apply(
        lambda row:
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=row['size'],
                color=row['KLEUR_LAMP'],
                fill=True,
                fill_color=row['KLEUR_LAMP'],
                fill_opacity=row['transparency'],
                weight=0,
            ).add_to(map),
            axis = 1
    )
    # Show in Streamlit
    st_map = st_folium(map, width=1150, height=900)

# App
def main():
    st.set_page_config(APP_TITLE, layout='wide')
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)
    
    # Load data
    df = pd.read_csv('./data/eindhoven_lighting_prepared_amira.csv')
    interactive_folium_map(df)

if __name__ == "__main__":
    main()


# Options
# map_overlay = st.checkbox('Interactive Map')
# st.write('# Options')
# st.write("Filter by:")
# stadsdeel = st.multiselect('Stadsdeel / District', df['STADSDEEL'].value_counts().index)
# wijk = st.multiselect('Wijk', df['WIJK'].value_counts().index)
# buurt = st.multiselect('Buurt', df['BUURT'].value_counts().index)
# straat = st.multiselect('Straatnaam', df['STRAATNAAM'].value_counts().index)

# if stadsdeel:
#     wijk = st.multiselect('Wijk', df[df['STADSDEEL'] == stadsdeel]['WIJK'].value_counts.index)
# if wijk:
#     buurt = st.multiselect('Buurt', df[df['WIJK'] == wijk]['BUURT'].value_counts.index)