import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static



df = pd.read_csv("data\data_timofey.csv")
# data prep


# Streamlit App
st.title("Cross-spatial districts")

col1, col2 = st.columns(2)

with col1:
    st.header('Select filters')
    avg_income_selected = st.checkbox("Average income", value=True)
    avg_house_value_selected = st.checkbox("Average house value")
    num_shops_selected = st.checkbox("Number of shops")
    num_residents_selected = st.checkbox("Number of residents")
    percent_unhappy_selected = st.checkbox("Percent unhappy")
    score_good_life_selected = st.checkbox("Goold life score")

with col2:
    st.header('Select values')

    if avg_income_selected:
        minVal = df['AvgIncome'].min()
        maxVal = df["AvgIncome"].max()
        avg_income_selected_score = st.slider("Select Average Income (Yearly)", min_value=minVal, max_value=maxVal, value=(minVal+maxVal)/2)
    
    if avg_house_value_selected:
        minVal = df['AvgHouseValue'].min()
        maxVal = df["AvgHouseValue"].max()
        avg_house_value_selected_score = st.slider("Select Average House Value", min_value=minVal, max_value=maxVal, value=(minVal+maxVal)/2)

    if num_shops_selected:
        minVal = df['NumberShops'].min()
        maxVal = df["NumberShops"].max()
        num_shops_selected_score = st.slider("Select Number of shops nearby", min_value=minVal, max_value=maxVal, value=(minVal+maxVal)/2)
    
    if num_residents_selected:
        minVal = df['number of residents'].min()
        maxVal = df["number of residents"].max()
        num_residents_selected_score = st.slider("Select Number of Residents", min_value=minVal, max_value=maxVal, value=(minVal+maxVal)/2)

    if percent_unhappy_selected:
        minVal = df['PctUnhappy'].min()
        maxVal = df["PctUnhappy"].max()
        percent_unhappy_selected_score = st.slider("Select percent unhappy", min_value=minVal, max_value=maxVal, value=(minVal+maxVal)/2)
    
    if score_good_life_selected:
        minVal = df['ScoreGoodLife'].min()
        maxVal = df["ScoreGoodLife"].max()
        score_good_life_selected_score = st.slider("Select good life score", min_value=minVal, max_value=maxVal, value=(minVal+maxVal)/2)


# Filter the DataFrame based on user selection
filtered_df = df
if avg_income_selected:
    filtered_df = filtered_df[filtered_df['AvgIncome'] > avg_income_selected_score]

if avg_house_value_selected:
    filtered_df = filtered_df[filtered_df['AvgHouseValue'] > avg_house_value_selected_score]

if num_shops_selected:
    filtered_df = filtered_df[filtered_df['NumberShops'] > num_shops_selected_score]

if num_residents_selected:
    filtered_df = filtered_df[filtered_df["number of residents"] > num_residents_selected_score]

if percent_unhappy_selected:
    filtered_df = filtered_df[filtered_df['PctUnhappy'] > percent_unhappy_selected_score]

if score_good_life_selected:
    filtered_df = filtered_df[filtered_df['ScoreGoodLife'] > score_good_life_selected_score]



# Create an interactive map using Folium

my_map = folium.Map(location=[51.45549394437564, 5.461942407429312], zoom_start=12)

# Add markers for each district in the filtered DataFrame
for index, row in filtered_df.iterrows():
    point = row['GeoshapeCenter']
    point_strings = point.split(",")
    points = [float(value) for value in point_strings]
    description = "<b style='font-size: 18px'>" + row['DistrictName'] + "</b><br>"
    if avg_income_selected:
        description += "Avg income: " + str(filtered_df["AvgIncome"][index]) + "<br>"
    if avg_house_value_selected:
        description += "Average house value: " + str(filtered_df["AvgHouseValue"][index]) + "<br>"
    if num_shops_selected:
        description += "Number of shops: " + str(filtered_df["NumberShops"][index]) + "<br>"
    if num_residents_selected:
        description += "Number of residents: " + str(filtered_df["number of residents"][index]) + "<br>"
    if percent_unhappy_selected:
        description += "Percent unhappy: " + str(filtered_df["PctUnhappy"][index]) + "<br>"
    if score_good_life_selected:
        description += "Good life score: " + str(filtered_df["ScoreGoodLife"][index]) + "<br>"
    
    folium.Marker(location=points, popup=folium.Popup(description, max_width=300), icon=folium.Icon(color='#CC112F')).add_to(my_map)

# Display the map in Streamlit
folium_static(my_map)
