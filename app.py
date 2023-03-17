
import streamlit as st
import pandas as pd
from PIL import Image

# print(st.__file__)


# data sources
aq_mostrecent = "./data/real-time-fijnstof-monitoring.csv" 
aq_locations = "./data/locaties_airboxen.csv"

# TODO
# Every websiteload (?) - or can we make a separate backend ?
# - check if most recent download is older than 1 hour or so; 
# if true, fill in aq_mostrecent with new data from all locations. 
# - drop data older than today
# - recompute max, min, generate text
#

# find MAX, MIN in the most recent AQ data
def aq_maxmin(): #TODO
    try:
        dfaq = pd.read_csv(aq_mostrecent,sep=";")
        dfaq = dfaq[["PM1","PM2.5","PM10","geopoint"]]
        # get the right locations from aq_locations
        return (dfaq["PM10"].max(),dfaq["PM10"].min(),"prof dr Dorgelolaan","Vossenbeemd") 
    except:
        return "ERROR: data problem"

# MAIN
def main():
    st.set_page_config(page_title='EDS' ,layout="wide",page_icon='')
    st.title("Eindhoven Data Stories")
    

##    col1,col2 = st.columns(2)
##    with col1:
##

# -------------------------------------
    # Daily news: Air quality
    st.subheader("Air quality today")
    val_max,val_min,where_max,where_min = aq_maxmin()
    st.write("The highest air pollution measured so far today was in {0} at 9:11, \n\
             most probably due to traffic.\n\
             The best air quality was in {1}, making this a 22 days -streak."
             .format(where_max, where_min)) #TODO add some emojis :-) 
    
# -------------------------------------
    # Daily news: Biodiversity challenge
    bc_soort = "Bonte dennenschildwants" # TODO: compute from the data, make a static CSV for the whole year .. 
    st.subheader("Challenge: find the "+ bc_soort)
    st.image(Image.open("./images/47123550.jpg"))
    st.write("In the last 3 years on this day, this endangered species has been seen in the Eindhoven area.\
             Read more about this observation <a href=\"{}\">here</a>."
             .format("https://waarneming.nl/observation/235848374/") )
    st.write("Can you find it again?") 
    with st.expander("Other endangered species found in previous years on this day:"):
        st.write("Loading..") #TODO

    #TODO: talk to waarneming.nl

# -------------------------------------
    st.subheader("Your question")
    st.write("If you have a question about (life in) Eindhoven that could be \
             investigated using data, write it here.")
    with st.form(key="question"):
        ta_question = st.text_area("... ?")
        question = st.form_submit_button("Ask EDS")
        #TODO: add name, email fields, check, save question to database
    with st.expander("Already asked.."):
        st.write("Loading..") #TODO

    st.info("Made and maintained @ Fontys ICT")

if __name__ == '__main__':
    main()



