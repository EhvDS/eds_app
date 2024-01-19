import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title('Eindhoven Neighborhoods puzzle')

iframe_html = """
<div style="width: 100%; height: 1080px; display: flex; justify-content: center;">
    <iframe src="https://oakwoodinnovations.nl/stijnschellekens" style="width: 90%; height: 100%; min-width: 1366px; border: none;" frameBorder="0"></iframe>
</div>
"""

components.html(iframe_html, height=1080)