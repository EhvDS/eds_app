import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title('Eindhoven Neighborhoods puzzle')
st.write('Try to solve the puzzle by dragging the pieces to their correct place.')
st.write('Once the puzzle is correctly solved, you get a pop-up message.')

components.html('<iframe src="https://fontys-ai.rob-rutjes.nl/" width="1550" height="1350" frameBorder="0"></iframe>', width=1550, height=1350)