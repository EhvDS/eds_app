import streamlit as st
from streamlit_pannellum import streamlit_pannellum

# Loading images
# TODO: group images per neighbourhood, find good storage location for the images
images = {
    "Philips Stadion": "https://i.imgur.com/PCogYkq.jpg",
    "Strijp-T": "https://i.imgur.com/zAPJhoc.jpg",
    "Catharinakerk": "https://i.imgur.com/v9JDK49.jpg"
}
image_keys = list(images.keys())

# Session state
if 'score' not in st.session_state: # number of correct guesses
    st.session_state.score = 0

if 'image_index' not in st.session_state: # image_index controls the image that is shown
    st.session_state.image_index = 0

if 'current_round' not in st.session_state: # image_index controls the image that is shown
    st.session_state.current_round = 1

n_rounds = 5
game_done = st.session_state.current_round > n_rounds

def cycle_image(): # TODO: make image selection random
    # Increase index or reset to 0 if max is reached
    if st.session_state.image_index < (len(image_keys)-1):
        st.session_state.image_index += 1
    else:
        st.session_state.image_index = 0

selected_image = images[ image_keys[st.session_state.image_index] ]
correct_neighbourhood = image_keys[ st.session_state.image_index ]

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
  selected_neighbourhood = st.selectbox('Which neighbourhood is this image located in?', (image_keys))
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

if game_done:
    st.header("Game Over")
    st.markdown("You guessed " + str(st.session_state.score) + " images correctly.")
    st.button("New Game", on_click=reset_game)