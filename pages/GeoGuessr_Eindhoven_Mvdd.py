import streamlit as st
import folium
import random
import geopandas as gpd
import ast
import os

from streamlit_pannellum import streamlit_pannellum
from streamlit_folium import st_folium
from shapely.ops import unary_union

def init():
    if 'points' not in st.session_state:  # number of correct guesses
        st.session_state.points = 0

    if 'diff' not in st.session_state:
        st.session_state.diff = "wijknaam"

    if 'needs_refresh' not in st.session_state:
        st.session_state.needs_refresh = True
        
    gdf, df_images = read_data()
        
    if 'seen_images' not in st.session_state:  # keep track of images seen this round to avoid duplicates
        st.session_state.seen_images = []

    if 'cur_image' not in st.session_state:
        st.session_state.cur_image = get_random_image(df_images)

    if 'cur_round' not in st.session_state:
        st.session_state.cur_round = 1
    
    return gdf, df_images

def retrieve_images(base_path):
    images = []

    for wijk_name in os.listdir(base_path):
        wijk_path = os.path.join(base_path, wijk_name)

        if os.path.isdir(wijk_path):
            for buurt_name in os.listdir(wijk_path):
                buurt_path = os.path.join(wijk_path, buurt_name)

                if os.path.isdir(buurt_path):
                    for image_file in os.listdir(buurt_path):
                        image_path = os.path.join(buurt_path, image_file)
                        images.append({
                            'wijknaam': wijk_name,
                            'buurtnaam': buurt_name,
                            'ImagePath': image_path
                        })

    return images

def get_random_image(images):
    # Filter out images that have already been seen
    available_images = [image for image in images if image['ImagePath'] not in st.session_state.seen_images]

    # Select a random image from the available images
    random_image = random.choice(available_images)

    # Add the selected image to the list of seen images
    st.session_state.seen_images.append(random_image['ImagePath'])

    return random_image

def check_guess(guess, number):
    if(st.session_state.cur_image[st.session_state.diff] == guess):
        st.markdown(":green[**Correct!**]")
        st.session_state.points += 1
    else:
        st.write(":red[**Wrong!**]")
        st.text("The answer was: " + str(st.session_state.cur_image[st.session_state.diff]))
    st.session_state.cur_round += 1
    load_new_image()

def load_new_image():
    st.session_state.cur_image = get_random_image(df_images)

def load_image():
    image_path = st.session_state.cur_image['ImagePath']
    return image_path

def read_data():
    gdf = load_regions()
    df_images = retrieve_images("images/GeoGuessr_Max")
    return gdf, df_images

def restart():
    st.session_state.cur_round = 1
    st.session_state.points = 0
    st.session_state.seen_images = []
    st.session_state.cur_image = get_random_image(df_images)

def load_regions():
    gdf = gpd.read_file("data/buurten_geoguessr_max.shp")
    gdf = gdf.groupby(st.session_state.diff)['geometry'].apply(unary_union).reset_index()
    gdf[st.session_state.diff] = gdf[st.session_state.diff].str.replace('Wijk', '', regex=False)
    gdf.crs = "EPSG:4326"
    return gdf

gdf, df_images = init()
col1, col2 = st.columns(2, gap="large")

with col1:
    st.header("GeoGuessr")
    st.subheader("by Max ")
with col2:
    if st.session_state.cur_round == 1:
        opt = st.selectbox(
        "Difficulty",
        ("Wijken", "Buurten"))
        if opt == "Wijken":
            st.session_state.diff = "wijknaam"
        elif opt == "Buurten":
            st.session_state.diff = "buurtnaam"
        gdf = load_regions()
        
st.header("Score: " + str(st.session_state.points) + " Points")
st.markdown("<style>iFrame[title='streamlit_pannellum.streamlit_pannellum']{ margin-bottom: -230px}</style>", unsafe_allow_html=True)

if st.session_state.cur_round <= 5:
    st.subheader("Round: " + str(st.session_state.cur_round) + " / 5")

    st.image(load_image())

    eindhoven_map = gdf.explore()

    guess = gdf[st.session_state.diff][0]

    #with st.form(key='map_form', border=False):
    st_data = st_folium(eindhoven_map, use_container_width=True, height=300, zoom=11)
        
    if st_data["last_object_clicked_tooltip"]:
        guess = str(st_data["last_object_clicked_tooltip"].split()[1:])
        list_of_words = ast.literal_eval(guess)
        guess = ' '.join(list_of_words)

    st.write("Guess: ", guess)
    st.button(label='Submit', on_click=check_guess, args=(guess, 1))
else:
    st.button("Play again!", on_click=restart())