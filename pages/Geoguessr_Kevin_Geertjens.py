from streamlit_pannellum import streamlit_pannellum
from streamlit_folium import st_folium
from streamlit_modal import Modal
from shapely import Polygon, Point

import streamlit as st
import folium
import pandas as pd
import json

def main():  
  st.set_page_config(layout="wide")

  # Loading images
  df_images = pd.read_csv("./data/kevin_geoguessr_images.csv", index_col=0)

  # Extracting map markers from most recent data
  df_latest_data = pd.read_csv("./data/mostrecent_data.csv")
  df_map_markers = pd.DataFrame(columns=['NbId', 'lon', 'lat'])

  for idx, row in df_latest_data.iterrows():
      split = row['GeoshapeCenter'].split(',')
      new_row = {'lat': float(split[0]), 'lon': float(split[1]), 'NbId': row['NbId']}
      df_map_markers = pd.concat([df_map_markers, pd.DataFrame(new_row, index=[idx])], ignore_index=True)

  df_map_markers = df_map_markers.set_index('NbId')
    
  # Session state
  if 'score' not in st.session_state: # number of correct guesses
      st.session_state.score = 0

  if 'current_image' not in st.session_state:
      st.session_state.current_image = df_images.sample()

  if 'images_seen' not in st.session_state: # keep track of images seen this round to avoid duplicates
      st.session_state.images_seen = []

  if 'current_round' not in st.session_state:
      st.session_state.current_round = 1

  if 'last_clicked' not in st.session_state:
          st.session_state.last_clicked = []

  if 'modal_text' not in st.session_state:
     st.session_state.modal_text = ""

  n_rounds = 5
  game_done = st.session_state.current_round > n_rounds

  selected_image = st.session_state.current_image['URL']
  selected_image = selected_image.tolist()[0]
  correct_neighbourhood = st.session_state.current_image['NbName']
  correct_neighbourhood = correct_neighbourhood.tolist()[0]

  modal = Modal("",
                key="round-result",
                padding=30,
                max_width=850
  )

  if modal.is_open():
    with modal.container():
        st.markdown(f'<p style="color:#000;font-size:24px;">{st.session_state.modal_text}</p>', unsafe_allow_html=True)

  # Header section
  st.title("Geoguessr in Eindhoven")
  st.markdown("""Play Geoguessr with locations throughout Eindhoven: You will be shown several 360 degree pictures, and you have to guess which neighbourhood in Eindhoven the pictures 
                were taken in. You can pan and zoom the image to look around.""")

  col1, col2 = st.columns(2)

  col1.subheader("Score: " + str(st.session_state.score) + " / " + str(n_rounds))
  col2.subheader("Round: " + str(min(st.session_state.current_round, n_rounds)) + " / " + str(n_rounds))

  st.markdown("#")

  # Panorama viewer & Map selection
  col3, col4 = st.columns(2)

  if not game_done:

    with col3:
      st.subheader("Where was this picture taken?")
      st.markdown("###")
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

    with col4:
      st.subheader("Select the correct neighbourhood:")
      st.markdown("##")

      m = folium.Map(location=[51.448, 5.465], tiles="OpenStreetMap", zoom_start=12)

      for idx, row in df_latest_data.iterrows():       
          geoshape = json.loads(row['Geoshape'])

          geojson = folium.GeoJson(
              geoshape, 
              tooltip=row['NbName'],

              style_function=lambda feature: {
                "fillColor": "#CC112F",
                "color": "#CC112F",
                "weight": 3,
              },

              highlight_function=lambda feature: {
                "weight": 4,
                "fillOpacity": 0.5
              }
          )

          geojson.add_to(m)

      folium_data = st_folium(m)
      last_object = folium_data['last_object_clicked']

      if last_object:
        marker = [last_object['lat'], last_object['lng']]

        if marker != st.session_state.last_clicked: # Otherwise any sort of map movement will trigger the check
          st.session_state.last_clicked = marker
          point = Point(marker)

          for idx, row in df_latest_data.iterrows():     
            geoshape = json.loads(row['Geoshape'])['coordinates'][0]
            coordinates = []

            for coord in geoshape:
                new_coord = tuple([coord[1], coord[0]]) # Coordinates have to be reversed
                coordinates.append(new_coord)

            polygon = Polygon(coordinates)
            if polygon.contains(point):
              check_answer(row['NbName'], correct_neighbourhood, df_images, modal)

  # Game Over display
  if game_done:
    st.header("Game Over")
    st.markdown("You guessed " + str(st.session_state.score) + " images correctly.")
    st.button("New Game", on_click=reset_game)

def cycle_image(image_dataset):
    # Randomly select new image, avoid images already shown this game
    new_image = image_dataset.sample()
    
    url_check = new_image['URL'].tolist()[0]
    while url_check in st.session_state.images_seen:
        new_image = image_dataset.sample()
        url_check = new_image['URL'].tolist()[0]

    st.session_state.images_seen.append(url_check)
    st.session_state.current_image = new_image

def check_answer(answer, correct_answer, image_dataset, modal):
      # Check answer given in selectbox, update score, and move to next image
      st.session_state.current_round += 1
      st.session_state.score += (answer.lower() == correct_answer.lower())

      cycle_image(image_dataset)

      st.session_state.modal_text = "You guessed correctly!" if (answer.lower() == correct_answer.lower()) else "Wrong. The correct neighbourhood was " + correct_answer + "."
      modal.open()

      st.rerun()

def reset_game():
    st.session_state.score = 0
    st.session_state.current_round = 1
    st.session_state.images_seen = []

main()