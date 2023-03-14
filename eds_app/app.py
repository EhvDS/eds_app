import streamlit as st
import pandas as pd

# print(st.__file__)

# data sources
aq_mostrecent = "data/real-time-fijnstof-monitoring.csv" 


# find MAX, MIN in the most recent AQ data
def aq_maxmin():
    dfaq = pd.read_csv(aq_mostrecent,sep=";")
    dfaq = dfaq[["PM1","PM2.5","PM10","geopoint"]]
    return (dfaq["PM1"].max())


# MAIN
def main():
    st.title("Eindhoven Data Stories")
    menu = ["Home","About"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice == "Home":
        st.subheader("what the data says..")
        col1,col2 = st.columns(2)
        with col1:
            maxmin = aq_maxmin()
            st.write("The worst PM1 concentration measured today is {}".format(maxmin))

        with col2:
            with st.form(key="question"):
                ta_question = st.text_area("Your data question here")
                question = st.form_submit_button("Ask EDS")

    else:
        st.subheader("About this site")
        st.info("Made and maintained @ Fontys ICT")

if __name__ == '__main__':
    main()



