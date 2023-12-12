import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import plotly.graph_objects as go
import numpy as np


df = pd.read_csv('./data/mostrecent_data.csv')
df_cor = df.drop(columns=['Geoshape', 'GeoshapePerimeter', 'GeoshapeArea', 'GeoshapeCenter', 'NbId', 'DistrictId'])
df_cor = df_cor.fillna(0)
st.write("# Correlations in Eindhoven based on education")
st.write("### Made by Stèphanie Smits")

#st.table(df_cor)

y_option = st.selectbox(
 'Select your first attribute',
  ('PctFeelsUnsafe', 'ScoreGoodLife', 'PctUnhappy', 'ScoreDiversity' 
   'AvgHouseValue', 'ScoreSocialCohesion', 'PctEconomicallyIndependent', 'PctUnemployed'))

st.write('You selected:', y_option)

x_option = st.selectbox(
 'Select your second attribute',
  ('PctLowEducation', 'PctHighEducation'))

st.write('You selected:', x_option)

fig = px.scatter(data_frame=df_cor, x=x_option, y=y_option, color="number of residents",
                 color_discrete_sequence=px.colors.qualitative.G10)


st.plotly_chart(fig)

fig2 = px.imshow(
  df_cor.corr(),
  color_continuous_scale="Reds",
)

st.plotly_chart(fig2)