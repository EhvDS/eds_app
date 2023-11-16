
import streamlit as st
import pandas as pd
from PIL import Image



# MAIN
def main():
    st.set_page_config(page_title='EDS' ,page_icon='')
    st.title("Eindhoven Data Stories")
    st.sidebar.success("Select a demo above.")

    st.markdown("Made and maintained @ Fontys ICT op donderdagavond.")

if __name__ == '__main__':
    main()



