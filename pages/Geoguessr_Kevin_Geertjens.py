import streamlit as st
from streamlit_pannellum import streamlit_pannellum
import pandas as pd
import random

# Loading images
df_images = pd.read_csv("./data/kevin_geoguessr_images.csv", index_col=0)

# Session state
if 'score' not in st.session_state: # number of correct guesses
    st.session_state.score = 0

if 'image_index' not in st.session_state: # image_index controls the image that is shown
    st.session_state.image_index = random.randint(0, len(df_images))

if 'images_seen' not in st.session_state: # keep track of images seen this round to avoid duplicates
    st.session_state.images_seen = []

if 'current_round' not in st.session_state: # image_index controls the image that is shown
    st.session_state.current_round = 1

n_rounds = 5
game_done = st.session_state.current_round > n_rounds

def cycle_image():
    # Randomly select new image, avoid images already shown this game
    new_index = random.randint(0, len(df_images))
    print(st.session_state.images_seen)
    while new_index in st.session_state.images_seen:
        new_index = random.randint(0, len(df_images))

    st.session_state.images_seen.append(new_index)
    st.session_state.image_index = new_index

selected_image = df_images.iloc[[st.session_state.image_index]]['URL']
selected_image = selected_image.tolist()[0]
correct_neighbourhood = df_images.iloc[[st.session_state.image_index]]['NbName']
correct_neighbourhood = correct_neighbourhood.tolist()[0]

# Header section
st.title("Geoguessr in Eindhoven")
st.markdown("""Play Geoguessr with locations throughout Eindhoven: You will be shown several 360 degree pictures, and you have to guess which neighbourhood in Eindhoven the pictures 
               were taken in. You can pan and zoom the image to look around.""")

col1, col2 = st.columns(2)
col1.subheader("Score: " + str(st.session_state.score) + " / " + str(n_rounds))
col2.subheader("Round: " + str(min(st.session_state.current_round, n_rounds)) + " / " + str(n_rounds))

st.markdown("#")

# Neighbourhood Selection
# TODO: show map of Eindhoven instead of basic selectbox
def check_answer(value):
    # Check answer given in selectbox, update score, and move to next image
    cycle_image()

    st.session_state.current_round += 1
    st.session_state.score += (value == correct_neighbourhood)

if not game_done:
  selected_neighbourhood = st.selectbox('Which neighbourhood is this image located in?', (df_images['NbName'].unique()))
  st.button("Confirm Neighbourhood", on_click=check_answer, args=(selected_neighbourhood,))

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
    st.session_state.image_index = 0
    st.session_state.score = 0
    st.session_state.current_round = 1
    st.session_state.images_seen = []

if game_done:
    st.header("Game Over")
    st.markdown("You guessed " + str(st.session_state.score) + " images correctly.")
    st.button("New Game", on_click=reset_game)