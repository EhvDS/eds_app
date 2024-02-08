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
                publicly available data about the :red[7 Eindhoven city areas (_stadsdelen_), 19 districts (_wijken_) and 109 neighbourhoods (_buurten_)].\
                Choose on the sidebar which one you want to see.")
    
    st.markdown("Made in winter 2023 at [Fontys ICT](https://www.fontysictinnovationlab.nl/) by students experimenting with data visualization.\
                All data and code is [available](https://github.com/EhvDS/eds_app) but not yet properly reviewed and checked. \
                So :red[please don't base any serious conclusions on these visualizations (yet)].")

    st.markdown("Send your questions and comments to Simona Orzan ([s.orzan@fontys.nl](mailto:s.orzan@fontys.nl)).")

    st.markdown("Enjoy!")

if __name__ == '__main__':
    main()


