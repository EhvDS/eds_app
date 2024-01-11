
import streamlit as st
import pandas as pd
from PIL import Image

# MAIN
def main():
    st.set_page_config(page_title='Eindhoven Data Stories' ,page_icon='')
    st.title("Eindhoven Data Stories")
    st.sidebar.success(".")

    st.markdown("Made and maintained at Fontys ICT by students experimenting with data visualization.")

if __name__ == '__main__':
    main()



