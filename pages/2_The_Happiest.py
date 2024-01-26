import streamlit as st
import pandas as pd
import folium
import branca.colormap as cm
import json

# df = pd.read_csv('data/happines_neighborhood_2022.csv')
df = pd.read_csv('data/full_happines_neighborhood_2022.csv')


def fix_data():
    # Drop the first row
    df = df[1:]
    # Rename columns
    df.columns = ['NbName', 'Unhappy people in %']
    # Remove rows with '.' in the 'Unhappy people in %' column
    df = df[df['Unhappy people in %'] != '.']
    # Convert 'Unhappy people in %' column to numeric
    df['Unhappy people in %'] = pd.to_numeric(df['Unhappy people in %'])
    # Save the data
    df.to_csv('data/happines_neighborhood_2022.csv', index=False)


def merge_data_with_cordinates():
    df2 = pd.read_csv('data/mostrecent_data.csv')
    merged_df = pd.merge(df, df2, on='NbName')
    merged_df.to_csv('data/full_happines_neighborhood_2022.csv', index=False)

# ------------------------------------------------------------------------------------------------------------------------------------


def create_map():
    # Convert GeoJSON strings to Python dictionaries
    df['Geoshape'] = df['Geoshape'].apply(json.loads)

    # Get the center coordinates from the first row
    center_lat, center_lon = df['Geoshape'][0]['coordinates'][0][0][1], df['Geoshape'][0]['coordinates'][0][0][0]

    # Create a map centered at the first point in the Geoshape coordinates
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # Define a function to assign colors based on 'Unhappy people in %' values
    def get_color(unhappiness):
        # Normalize the value to be in the range [0, 1]
        normalized_value = (unhappiness - 1) / 11
        # Use a linear color gradient from green to yellow to red
        color_gradient = cm.LinearColormap(
            ['green', 'orange', 'red'], vmin=0, vmax=1)
        return color_gradient(normalized_value)

    # Define a function to assign icons based on 'Unhappy people in %' values
    def get_icon(unhappiness):
        if unhappiness <= 3:
            return 'smile'
        elif 4 <= unhappiness <= 6:
            return 'meh'
        elif 7 <= unhappiness <= 9:
            return 'neutral'
        else:
            return 'frown'

    # Add GeoJSON layer to the map with colors and icons
    for index, row in df.iterrows():
        color = get_color(row['Unhappy people in %'])
        icon = get_icon(row['Unhappy people in %'])

        # Replace the tooltip content with the neighborhood name and face icon
        tooltip_content = (
            f"<p style='font-size:16px; text-align:center; font-weight:bold;'>{row['NbName']}</p>"
            f"<p style='font-size:24px; text-align:center;'>"
        )
        if icon == 'smile':
            tooltip_content += "😄"  # Happy face
        elif icon == 'meh':
            tooltip_content += "😊"  # Smiley face
        elif icon == 'neutral':
            tooltip_content += "😐"  # Neutral face
        else:
            tooltip_content += "😭"  # Sad face
        tooltip_content += "</p>"

        folium.GeoJson(
            row['Geoshape'],
            name=row['NbName'],
            style_function=lambda feature, color=color: {
                'fillColor': color,
                'color': 'gray',
                'weight': 2,
                'fillOpacity': 0.6,
            },
            tooltip=tooltip_content
            ### icon=folium.Icon(color=color, icon=icon, icon_size=(50, 50)).to_dict(),  # Change the numbers for adjusting the icon size <-- ERROR, icon not an argument in GeoJson, needs to be added as a separate layer
        ).add_to(m)

    # Save the map to an HTML file
    m.save('map_interactive_gradient.html')
    with open('map_interactive_gradient.html', 'r', encoding='utf-8') as file:
        return file.read()


# Streamlit code
st.header("The Happiness Map of Eindhoven")
st.subheader("by Momchil Valkov")
st.write("""
    This interactive map offers an engaging visualization of neighborhood happiness in Eindhoven, utilizing official city data from 2022.  
            The map uses emoticons as indicators of happiness levels, rather than displaying raw percentages:
- 😄 (Happy Face): Represents areas with the lowest unhappiness scores, indicating high levels of contentment.
- 😊 (Smiley Face): Used for neighborhoods with moderate unhappiness scores.
- 😐 (Neutral Face): Depicts areas with middle-range unhappiness scores.
- 😭 (Sad Face): Marks neighborhoods with the highest levels of unhappiness.  
            """)
map_html = create_map()
st.components.v1.html(map_html, width=900, height=800)
st.write("""
    This approach provides a user-friendly and visually appealing method to interpret the well-being of different communities within Eindhoven.  
    The project demonstrates the effectiveness of innovative data visualization techniques in urban and social research, making complex data easily accessible and understandable.
        """)
