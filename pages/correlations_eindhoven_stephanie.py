from os import write
import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import plotly.graph_objects as go
import numpy as np
import re


df_cor = pd.read_csv('./data/mostrecent_data_stephanie.csv')
df_cor = df_cor.fillna(0)
df_cor = df_cor.replace('.' , 0)
df_scatter = df_cor
st.write("# Correlations in Eindhoven: discover yourself!")
st.write("### Made by Stèphanie Smits")
st.write('##')
st.write("On this page, multiple data points are collected about the living circumstances in Eindhoven. Play with it yourself and see what interesting correlations you can find!")
st.write('##')
#st.table(df_cor.dtypes)
#st.table(df_scatter.dtypes)
#st.table(df_cor)

cols = ['number of residents', 'ScoreDiversity', 'NumberHouseholds',
       'AvgHouseValue', 'PctComplainsAQ', 'PctComplainsNoise',
       'AvgElectricityUsage', 'PctUnhappy', 'PctHighEducation',
       'PctLowEducation', 'PctFeelsUnsafe', 'ScoreSocialCohesion',
       'ScoreGoodLife', 'PctUnemployed', 'PctEconomicallyIndependent',
       'AvgIncome', 'NumberShops']



### scatterplot ###
 
y_option = st.selectbox(
 'Select your first attribute',
  (cols))

st.write('You selected:', y_option)

x_option = st.selectbox(
 'Select your second attribute',
  (cols))

st.write('You selected:', x_option)

c_option = st.selectbox(
 'Select if your want the data based on the living area or the amount of residents per living area',
  ('NbName', 'number of residents'))

st.write('You selected:', y_option)
st.write('##')


cc = np.corrcoef(df_scatter[y_option].values, df_scatter[x_option].values)[0,1].round(decimals=2)

if y_option == x_option:
    st.write('##### Try to select two different columns!')
elif cc < 0.6:
    st.markdown(f"##### The correlation coefficient is :red[{cc}], which indicates a weak correlation between the {y_option} and the {x_option}")
elif cc >= 0.75:
    st.markdown(f"##### The correlation coefficient is :green[{cc}], which indicates a strong correlation between the {y_option} and the {x_option}")
else:
    st.markdown(f"##### The correlation coefficient is :blue[{cc}], which indicates a normal correlation between the {y_option} and the {x_option}")



fig = px.scatter(data_frame=df_scatter, x=x_option, y=y_option, color=c_option,
                 color_continuous_scale="Reds", trendline="ols", trendline_color_override="white")

st.plotly_chart(fig)



### heatmap ###

# fig2 = px.imshow(
#   df_cor.corr(),
#   color_continuous_scale="Reds",
#   text_auto = True,
#   aspect = "auto"
# )

# st.plotly_chart(fig2)