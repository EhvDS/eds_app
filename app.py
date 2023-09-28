
import streamlit as st
import pandas as pd
from PIL import Image



# MAIN
def main():
    st.set_page_config(page_title='EDS' ,page_icon='')
    st.title("Eindhoven Data Stories")
    st.sidebar.success("Select a demo above.")

# -------------------------------------
    # Story: what makes people happy in Ehv
#    st.subheader("The happiest")
 #   st.markdown('by _Frits,Frits,Frits_, data: Open Data Eindhoven',
  #              unsafe_allow_html=True)
   # st.write ("An article about where the happiest people live in Eindhoven and what seems to influence this most.")
    
    st.markdown("Made and maintained @ Fontys ICT")

if __name__ == '__main__':
    main()



