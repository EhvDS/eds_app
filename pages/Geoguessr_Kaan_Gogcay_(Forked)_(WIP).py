
# cd "source\repos\Jupyter-Notebooks\Semester 6\eds_app\pages"
# C:\Users\kaan-\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\streamlit.exe run Geoguessr_Kaan_Gogcay.py

import streamlit as state_29048  # some random numbers to not fuck with others' app
from streamlit_pannellum import streamlit_pannellum
import pandas as pd
import random


def main():

    # Loading images
    df_images = pd.read_csv("./data/kevin_geoguessr_images.csv", index_col=0)

    # Session state
    if 'score' not in state_29048.session_state:  # number of correct guesses
        state_29048.session_state.score = 0

    if 'current_image' not in state_29048.session_state:
        state_29048.session_state.current_image = df_images.sample()

    # keep track of images seen this round to avoid duplicates
    if 'images_seen' not in state_29048.session_state:
        state_29048.session_state.images_seen = []

    if 'current_round' not in state_29048.session_state:
        state_29048.session_state.current_round = 1

    if 'previous_correct_value' not in state_29048.session_state:
        state_29048.session_state.previous_correct_value = ""

    if 'answered_value' not in state_29048.session_state:
        state_29048.session_state.answered_value = ""

    # Variables
    n_rounds = 5
    game_done = (state_29048.session_state.current_round > n_rounds)

    selected_image = state_29048.session_state.current_image['URL']
    selected_image = selected_image.tolist()[0]
    correct_neighbourhood = state_29048.session_state.current_image['NbName']
    correct_neighbourhood = correct_neighbourhood.tolist()[0]

    # Header section
    state_29048.title("Geoguessr Eindhoven (Hood Edition)")
    state_29048.markdown("""In the Geoguessr Eindhoven Hood Edition you will be shown 360° images. The majority of the images shown are known for iconic hang-out spots for teens. You can pan and zoom in the images. It's important to note that you have to guess the location from YOUR perspective, NOT what you are seeing a kilometer in the back.""")

    state_29048.markdown("#")
    state_29048.markdown("#")

    col1, col2 = state_29048.columns(2)
    col1.subheader("Score: " + str(state_29048.session_state.score) +
                   " / " + str(n_rounds))
    col2.subheader("Round: " + str(min(state_29048.session_state.current_round,
                                       n_rounds)) + " / " + str(n_rounds))

    # Display the correct answer below the panorama viewer only when the button is clicked
    if state_29048.session_state.answered_value is not "":
        if state_29048.session_state.answered_value == state_29048.session_state.previous_correct_value:
            state_29048.header(
                f"Correct! The answer was {state_29048.session_state.previous_correct_value}.")
        else:
            state_29048.header(
                f"Wrong! The correct answer was {state_29048.session_state.previous_correct_value}.")

    if not game_done:
        selected_neighbourhood = state_29048.selectbox(
            'Which neighbourhood is this image located in?', (df_images['NbName'].unique()))
        state_29048.button("Confirm Neighbourhood", on_click=check_answer, args=(
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
        state_29048.header("Game Over")
        state_29048.markdown("You guessed " + str(state_29048.session_state.score) +
                             " images correctly.")
        state_29048.button("New Game", on_click=reset_game)


def reset_game():
    state_29048.session_state.score = 0
    state_29048.session_state.current_round = 1
    state_29048.session_state.images_seen = []
    state_29048.session_state.answered_value = ""
    state_29048.session_state.previous_correct_value = ""


def cycle_image(df_images):
    # Randomly select new image, avoid images already shown this game
    new_image = df_images.sample()
    url_check = new_image['URL'].tolist()[0]
    while url_check in state_29048.session_state.images_seen:
        new_image = df_images.sample()
        url_check = new_image['URL'].tolist()[0]

    state_29048.session_state.images_seen.append(url_check)
    state_29048.session_state.current_image = new_image


def check_answer(selected_neighbourhood, df_images, correct_neighbourhood):
    # ...
    state_29048.session_state.answered_value = selected_neighbourhood
    state_29048.session_state.previous_correct_value = correct_neighbourhood

    # next image
    cycle_image(df_images)

    # Check answer given in selectbox, update score
    state_29048.session_state.current_round += 1
    state_29048.session_state.score += (selected_neighbourhood ==
                                        correct_neighbourhood)


main()
