import streamlit as st
import pandas as pd
import pydeck as pdk

# Load data
df = pd.read_csv("data/Eindhoven_by_night_data_Mat.csv")

def categorize_sound_level(value):
    if value < 50:
        return [0, 255, 0, 160], 'Quiet'  # Green for quiet
    elif 50 <= value < 60:
        return [255, 255, 0, 160], 'Moderate'  # Yellow for moderate
    else:
        return [255, 0, 0, 160], 'Noisy'  # Red for noisy

# Apply the categorization function to create new columns for color and label
df['color'], df['label'] = zip(*df['Overall Avg soundlevel(LAeq)'].apply(categorize_sound_level))

# Pre-format the tooltip content with line breaks
df['tooltip_content'] = df.apply(lambda row: f"<b>Sound Level:</b> {row['Overall Avg soundlevel(LAeq)']:.2f} dB<br><b>Category:</b> {row['label']}<br><b>Location:</b> {row['beschrijving locatie']}", axis=1)

# Scale the radius based on the sound level
df['radius'] = df['Overall Avg soundlevel(LAeq)'] * 4  # Adjust the scaling factor as needed

# Set up the scatter plot layer
scatterplot_layer = pdk.Layer(
    'ScatterplotLayer',
    df,
    get_position='[longitude, latitude]',
    get_color='color',
    get_radius='radius',
    pickable=True,  # Enable layer to be pickable for tooltips
)

# Define tooltip with custom style
tooltip = {
    "html": "{tooltip_content}",
    "style": {
        "backgroundColor": "steelblue",
        "color": "white",
        "fontSize": "14px",  # Reduce font size
        "maxWidth": "180px",  # Set maximum width
        "padding": "5px"      # Adjust padding
    }
}

# Set the viewport location
view_state = pdk.ViewState(
    latitude=df['latitude'].mean(),
    longitude=df['longitude'].mean(),
    zoom=11,
    pitch=0,
)

# Render the deck.gl map with the scatter plot layer
r = pdk.Deck(
    layers=[scatterplot_layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style='mapbox://styles/mapbox/satellite-v9'  # Satellite map style
)

#-------------------------------------------------------------------------

# Title of the app
st.header("Urban Symphony: Eindhoven's 30-Day Sound Story")
st.subheader("by Matthew da Silva")

# Use columns to place text beside the map
col1, col2 = st.columns([1, 2])

with col1:
    st.header("What's This Map All About?")
    st.write("""
        Let me give you a tour of this cool interactive map. 
        It's all about the hustle and bustle of Eindhoven, but in decibels! There are 
        19 sound sensors placed around the city – from the lively streets downtown to the 
        quieter, suburbs. These little gadgets have been eavesdropping on the city's 
        sounds for the past month, capturing the highs and lows of the urban symphony.
    """)

with col2:
    st.pydeck_chart(r)  # Display the map

# Text below the map
st.header("Colorful Insights")
st.write("""
    Each sensor on the map is like a mini artist, painting the city in sounds. 
    A splash of green shows areas where you can hear a pin drop (under 50 dB), 
    yellow spots are a bit buzzier (between 50 and 60 dB), and red areas? Well, 
    they're the life of the party, noise-wise (above 60 dB). And get this – the 
    louder the area, the bigger the dot on the map. Pretty handy, right?
""")

st.header("Why This Rocks")
st.write("""
    So, why is it useful? If you're a city planner or an environment activist, this 
    map is like a treasure map to make Eindhoven even more awesome. It's perfect 
    for pinpointing those ear-buzzing spots that might need a bit of a hush. And if 
    you're just wandering around or looking for a new place to call home, it's a 
    great way to find your perfect sound oasis. Go on, give it a try and see how 
    Eindhoven sounds!
""")