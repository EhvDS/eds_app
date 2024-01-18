import streamlit as st
import pandas as pd
import random
import geopandas as gpd
import branca.colormap as cm
import folium
import json
import numpy as np
from shapely.geometry import Polygon
# from sklearn import preprocessing
from streamlit_folium import st_folium

print('==== start ====')

# Data loading
df_mostrecent = pd.read_csv('./data/mostrecent_data_david.csv')
df_fullhapp = pd.read_csv('./data/full_happines_neighborhood_2022_david.csv')


# Data Cleaning & Augmenting
## Replace zeroes with NaN for accurate mean calculation
df_mostrecent['ScoreGoodLife'] = df_mostrecent['ScoreGoodLife'].replace(0, np.nan)
## normalizing number of residents to obtain color gradient later
df_fullhapp['number_of_residents_normalized'] = (df_fullhapp['number of residents'] - df_fullhapp['number of residents'].min()) / (df_fullhapp['number of residents'].max() - df_fullhapp['number of residents'].min())
## finding highest average income neighborhood
df_fullhapp['AvgIncome'] = df_fullhapp['AvgIncome'].str.replace(',', '.')
df_fullhapp['AvgIncome'] = pd.to_numeric(df_fullhapp['AvgIncome'])
idx_max_avgincome = df_fullhapp['AvgIncome'].astype('float').idxmax()
## actually loading the json coordinates instead of treating it as a string
df_fullhapp['Geoshape'] = df_fullhapp['Geoshape'].apply(json.loads)

polygons = []
for value in df_fullhapp['Geoshape']:
    coords = value['coordinates'][0]
    polygons.append(Polygon(coords))
df_fullhapp['Polygon'] = polygons

gdf_fullhapp = gpd.GeoDataFrame(df_fullhapp, geometry="Polygon", crs="EPSG:4326")
# print(gdf_fullhapp)

# Variable declaration
## General variables
number_of_questions = 3
## Stateful variables
if 'question_scores' not in st.session_state:
    st.session_state['question_scores'] = list()
    for i in range(0, number_of_questions):
        st.session_state['question_scores'].append(-1)

if 'question_page' not in st.session_state:
    st.session_state['question_page'] = 0

# Functions
def change_question(increment):
    st.session_state['question_page'] += increment

def check_correct(choice):
    if str(choice) == str(question_answers[st.session_state['question_page']]):
        st.session_state['question_scores'][st.session_state['question_page']] = 1
    else:
        st.session_state['question_scores'][st.session_state['question_page']] = 0

def get_color(residents):
        # Use a linear color gradient from green to yellow to red
        color_gradient = cm.LinearColormap(
            ['white', 'gray', 'black'], vmin=0, vmax=1)
        return color_gradient(residents)

# QUIZ questions + answers
## Questions
questions = ["Which measure has the strongest positive correlation with a neighborhood's average Good Life Score?",
                "Which of these neighborhoods has the highest average income per resident?",
                "What district is the most c?"]

## Multiple choices
question_choices = [["Average income per resident", "Average social cohesion score", "Percentage of financially independent residents", "Percentage of noise complaints"],
                    ['a', 'b', 'c', 'd'],
                    [5, 6, 7, 8]]

## Correct answers
question_answers = ["Average social cohesion score", 
                    "Karpen",
                    ""]

## Question Media
### Question 1 media
good_life_mean = df_mostrecent.groupby('NbName')['ScoreGoodLife'].mean()

### Question 2 media

#### Get the center coordinates from the first row
center_lat, center_lon = df_fullhapp['Geoshape'][0]['coordinates'][0][0][1], df_fullhapp['Geoshape'][0]['coordinates'][0][0][0]
#### Create a map centered at the first point in the Geoshape coordinates
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
popup = folium.GeoJsonPopup(
    fields=["NbName"],
    aliases=[""],
    localize=True,
    labels=True,
    style="background-color: yellow;",
)
tooltip = folium.GeoJsonTooltip(
    fields=["NbName", "number of residents"],
    aliases=["Neighborhood ", "Number of residents "],
    localize=True,
    sticky=True,
    labels=True
)
geo_j = folium.GeoJson(
    gdf_fullhapp,
    style_function=lambda features : {
        'fillColor': 'white',
        'color': 'blue',
        'weight': 2,
        'fillOpacity': 0.6,
    },
    popup=popup,
    tooltip=tooltip
).add_to(m)

### Question 3 media



# ========================= DOM elements / Page layout =========================
st.title('Quiz Time!')
st.subheader(f"Score: {sum(1 for x in st.session_state['question_scores'] if x == 1)}/{number_of_questions} Correct")
st.subheader(f"Question {st.session_state['question_page']+1}:")
st.header(questions[st.session_state['question_page']])



## TODO Question media goes here
if st.session_state['question_page'] == 0:
    st.bar_chart(good_life_mean)

    ## Answer layout
    container = st.container(border=True)
    col1, col2 = container.columns(2)
    ## Answer position randomizer
    choices = random.sample(question_choices[st.session_state['question_page']], 4)

    # Answers
    with col1:
        st.button(label = str(choices[0]), on_click=check_correct, args=[str(choices[0])])
        st.button(label = str(choices[1]), on_click=check_correct, args=[str(choices[1])])
    with col2:
        st.button(label = str(choices[2]), on_click=check_correct, args=[str(choices[2])])
        st.button(label = str(choices[3]), on_click=check_correct, args=[str(choices[3])])

elif st.session_state['question_page'] == 1:
    st_data = st_folium(m, width=800)
    st.caption('Neighborhoods colored by number of residents (darker shades indicate more residents)')
    choice = st_data['last_object_clicked_popup'].strip() if st_data['last_object_clicked_popup'] != None else ""
    st.button(label = "Submit", on_click=check_correct, args=[choice], disabled=choice == "")
elif st.session_state['question_page'] == 2:
    print(2)



# Question Navigation layout
col3, col4 = st.columns(2)

# Question navigation buttons
with col3:
    if st.session_state['question_page'] > 0:
        st.button('Previous Question', on_click=change_question, args=[-1], disabled=st.session_state['question_page'] <= 0)
with col4:
    if st.session_state['question_page'] < number_of_questions-1:
        st.button('Next Question', type='primary', on_click=change_question, args=[1], disabled=st.session_state['question_scores'][st.session_state['question_page']] == -1)

# TODO Remove DEBUG writes below 
st.write(st.session_state['question_page'])
st.write(st.session_state['question_scores'])
