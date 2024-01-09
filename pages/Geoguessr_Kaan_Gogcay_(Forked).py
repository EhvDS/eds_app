
# cd "source\repos\Jupyter-Notebooks\Semester 6\eds_app\pages"
# C:\Users\kaan-\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\streamlit.exe run "Geoguessr_Kaan_Gogcay_(Forked).py"

import streamlit as st
from streamlit_pannellum import streamlit_pannellum
import pandas as pd
import random


def main():

    # Loading images
    df_images = pd.read_csv("./data/kaan_geoguessr_images.csv", index_col=0)

    # Session state
    if 'score2' not in st.session_state:  # number of correct guesses
        st.session_state.score2 = 0

    if 'current_image2' not in st.session_state:
        st.session_state.current_image2 = df_images.sample()

    if 'images_seen2' not in st.session_state:  # keep track of images seen this round to avoid duplicates
        st.session_state.images_seen2 = []

    if 'current_round2' not in st.session_state:
        st.session_state.current_round2 = 1

    if 'previous_correct_value' not in st.session_state:
        st.session_state.previous_correct_value = ""

    if 'answered_value' not in st.session_state:
        st.session_state.answered_value = ""

    # Variables
    n_rounds = 5
    game_done = (st.session_state.current_round2 > n_rounds)

    selected_image = st.session_state.current_image2['URL']
    selected_image = selected_image.tolist()[0]
    correct_neighbourhood = st.session_state.current_image2['NbName']
    correct_neighbourhood = correct_neighbourhood.tolist()[0]

    # Header section
    st.title("Geoguessr Eindhoven (Hood Edition)")
    st.markdown("""In the Geoguessr Eindhoven Hood Edition you will be shown 360° images. The majority of the images shown are known for iconic hang-out spots for teens. You can pan and zoom in the images. It's important to note that you have to guess the location from YOUR perspective, NOT what you are seeing a kilometer in the back.""")

    st.markdown("#")
    st.markdown("#")

    col1, col2 = st.columns(2)
    col1.subheader("Score: " + str(st.session_state.score2) +
                   " / " + str(n_rounds))
    col2.subheader("Round: " + str(min(st.session_state.current_round2,
                                       n_rounds)) + " / " + str(n_rounds))

    # Display the correct answer below the panorama viewer only when the button is clicked
    if st.session_state.answered_value is not "":
        if st.session_state.answered_value == st.session_state.previous_correct_value:
            st.header(
                f"Correct! The answer was {st.session_state.previous_correct_value}.")
        else:
            st.header(
                f"Wrong! The correct answer was {st.session_state.previous_correct_value}.")

    if not game_done:
        selected_neighbourhood = st.selectbox(
            'Which neighbourhood is this image located in?', (df_images['NbName'].unique()))
        st.button("Confirm Neighbourhood", on_click=check_answer, args=(
            selected_neighbourhood, df_images, correct_neighbourhood))

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
    if game_done:
        st.header("Game Over")
        st.markdown("You guessed " + str(st.session_state.score2) +
                    " images correctly.")
        st.button("New Game", on_click=reset_game)


def reset_game():
    st.session_state.score2 = 0
    st.session_state.current_round2 = 1
    st.session_state.images_seen2 = []
    st.session_state.answered_value = ""
    st.session_state.previous_correct_value = ""


def cycle_image(df_images):
    # Randomly select new image, avoid images already shown this game
    new_image = df_images.sample()
    url_check = new_image['URL'].tolist()[0]
    while url_check in st.session_state.images_seen2:
        new_image = df_images.sample()
        url_check = new_image['URL'].tolist()[0]

    st.session_state.images_seen2.append(url_check)
    st.session_state.current_image2 = new_image


def check_answer(selected_neighbourhood, df_images, correct_neighbourhood):
    # ...
    st.session_state.answered_value = selected_neighbourhood
    st.session_state.previous_correct_value = correct_neighbourhood

    # next image
    cycle_image(df_images)

    # Check answer given in selectbox, update score
    st.session_state.current_round2 += 1
    st.session_state.score2 += (selected_neighbourhood == correct_neighbourhood)


main()
