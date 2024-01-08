# show an image
# make a guess -> make it a box wherein yuo can type but also just drop thing
# after a guess make an automised fact about the hood -> take most extreme value and generate a fact
# next img

# C:\Users\kaan-\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\streamlit.exe
# cd "source\repos\Jupyter-Notebooks\Semester 6\eds_app\pages"
# C:\Users\kaan-\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\streamlit.exe run Geoguessr_Kaan_Gogcay.py

import streamlit as st
from streamlit_pannellum import streamlit_pannellum
import pandas as pd
import random

# Loading images
df_images = pd.read_csv("./data/kaan_geoguessr_images.csv", index_col=0)

# Session state
if 'score' not in st.session_state:  # number of correct guesses
    st.session_state.score = 0

if 'current_image' not in st.session_state:
    st.session_state.current_image = df_images.sample()

if 'images_seen' not in st.session_state:  # keep track of images seen this round to avoid duplicates
    st.session_state.images_seen = []

if 'current_round' not in st.session_state:
    st.session_state.current_round = 1

n_rounds = 5
game_done = st.session_state.current_round > n_rounds


def cycle_image():
    # Randomly select new image, avoid images already shown this game
    new_image = df_images.sample()

    print(st.session_state.images_seen)
    url_check = new_image['URL'].tolist()[0]
    while url_check in st.session_state.images_seen:
        new_image = df_images.sample()
        url_check = new_image['URL'].tolist()[0]

    st.session_state.images_seen.append(url_check)
    st.session_state.current_image = new_image


selected_image = st.session_state.current_image['URL']
selected_image = selected_image.tolist()[0]
correct_neighbourhood = st.session_state.current_image['NbName']
correct_neighbourhood = correct_neighbourhood.tolist()[0]

# Header section
st.title("Geoguessr Eindhoven (Hood Edition)")
st.markdown("""In the Geoguessr Eindhoven Hood Edition you will be shown 360° images. The majority of the images shown are known for iconic hang-out spots for teens. You can pan and zoom in the images. It's important to note that you have to guess the location from YOUR perspective, NOT what you are seeing a kilometer in the back.""")

col1, col2 = st.columns(2)
col1.subheader("Score: " + str(st.session_state.score) + " / " + str(n_rounds))
col2.subheader("Round: " + str(min(st.session_state.current_round,
               n_rounds)) + " / " + str(n_rounds))

st.markdown("#")


def check_answer(value):
    # Check answer given in selectbox, update score, and move to next image
    cycle_image()

    st.session_state.current_round += 1
    st.session_state.score += (value == correct_neighbourhood)


if not game_done:
    selected_neighbourhood = st.selectbox(
        'Which neighbourhood is this image located in?', (df_images['NbName'].unique()))
    st.button("Confirm Neighbourhood", on_click=check_answer,
              args=(selected_neighbourhood,))

# Panorama viewer
if not game_done:
    streamlit_pannellum(
        config={
            "default": {
                "firstScene": "first",
            },
            "scenes": {
                "first": {
                    "type": "equirectangular",
                    "panorama": selected_image,
                    "autoLoad": True,
                    "disabled": True
                }
            }
        }
    )

# Game Over display


def reset_game():
    st.session_state.score = 0
    st.session_state.current_round = 1
    st.session_state.images_seen = []


if game_done:
    st.header("Game Over")
    st.markdown("You guessed " + str(st.session_state.score) +
                " images correctly.")
    st.button("New Game", on_click=reset_game)
