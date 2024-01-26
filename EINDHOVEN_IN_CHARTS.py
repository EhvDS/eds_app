import streamlit as st

# MAIN
def main():
    st.set_page_config(
        page_title='Eindhoven Data Stories' ,
        page_icon='',   
        layout="wide",
        initial_sidebar_state="expanded")

    st.title("Eindhoven Data Stories")
    st.sidebar.success("Choose ^^^")

    st.markdown("This is a collection of interactive charts, maps and small games based on publicly available data about the **Eindhoven city districts and neighbourhoods**.")
    st.markdown("Made and maintained at [Fontys ICT](https://www.fontysictinnovationlab.nl/) by students experimenting with data visualization.")
    st.markdown("Enjoy!")

if __name__ == '__main__':
    main()

