import streamlit as st

# MAIN
def main():
    st.set_page_config(
        page_title='Eindhoven Data Stories' ,
        page_icon='',   
        layout="wide",
        initial_sidebar_state="expanded")

    st.title("Eindhoven Data Stories")
    ##st.sidebar.success("Choose ^^^")

    st.markdown("This is a collection of interactive charts, maps and small games based on \
                publicly available data about the **Eindhoven city districts and neighbourhoods**.\
                Choose on the sidebar which one you want to see.")
    
    st.markdown("Made in winter 2023 at [Fontys ICT](https://www.fontysictinnovationlab.nl/) by students experimenting with data visualization.\
                All data and code is [available](https://github.com/EhvDS/eds_app) but not yet properly reviewed and checked. \
                So __please don't base any serious conclusions on these visualizations (yet)__.")

    st.markdown("Send your questions and comments to Simona Orzan ([s.orzan@fontys.nl](mailto:s.orzan@fontys.nl)).")

    st.markdown("Enjoy!")

if __name__ == '__main__':
    main()

