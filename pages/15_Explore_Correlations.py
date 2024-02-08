from os import write
import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import plotly.graph_objects as go
import numpy as np
import re


df_cor = pd.read_csv('./data/mostrecent_data_stephanie.csv')
df_cor = df_cor.fillna(0)
df_cor = df_cor.replace('.' , 0)
df_scatter = df_cor
st.header("Correlations in Eindhoven: discover yourself!")
st.subheader("by Stèphanie Smits")
st.write('##')
###st.write("The correlation coefficient is a measure of the closeness of association of the points in a scatter plot to a linear regression line based on those points. Possible values of the correlation coefficient range from -1 to +1, with -1 indicating a perfectly negative association and +1 indicating a perfectly positive association between two data points. A correlation coefficient close to 0 suggests little, if any, association.")
###st.image("images/corcoefs.png",width=400)
###st.markdown("Source: [The Correlation Coefficient](https://sphweb.bumc.bu.edu/otlt/MPH-Modules/PH717-QuantCore/PH717-Module9-Correlation-Regression/PH717-Module9-Correlation-Regression4.html)")
###st.write('##')
st.write("On this page, data about the living circumstances in Eindhoven is collected, and aggregated at the neighbourhood level. \
         The dataset contains parameters like the average house value (AvgHouseValue),percentage of highly educated people (PctHighEducation), \
         the score residents give to their life (ScoreGoodLife) etc. Click on the dropdown menus to see the whole list.")
st.write("##")
st.write("This allows for visualizing the relations between the parameters and see what the data says.") 
st.write("Each circle in the visualization below represents a neighbourhood. The size is proportional to the number of residents, the color indicated the city area.\
         On the X and Y axes, you can choose below which variables you'd like to check.\
         Play with it yourself and see what interesting correlations you can find!")
st.write('##')

cols = ['number of residents', 'ScoreDiversity', 'NumberHouseholds',
       'AvgHouseValue', 'PctComplainsAQ', 'PctComplainsNoise',
       'AvgElectricityUsage', 'PctUnhappy', 'PctHighEducation',
       'PctLowEducation', 'PctFeelsUnsafe', 'ScoreSocialCohesion',
       'ScoreGoodLife', 'PctUnemployed', 'PctEconomicallyIndependent',
       'AvgIncome', 'NumberShops']


 
y_option = st.selectbox(
 'Select your first attribute',
  (cols),index=5)

##st.write('You selected:', y_option)

x_option = st.selectbox(
 'Select your second attribute',
  (cols),index=3)

##st.write('You selected:', x_option)



cc = np.corrcoef(df_scatter[y_option].values, df_scatter[x_option].values)[0,1].round(decimals=2)

if y_option == x_option:
    st.write('##### Try to select two different columns!')
elif cc == 1.0:
    st.markdown(f"##### The correlation coefficient is :green[{cc}], which indicates a :green[perfect positive association] between the {y_option} and the {x_option}")
elif cc >= 0.9:
    st.markdown(f"##### The correlation coefficient is :green[{cc}], which indicates a :green[very strong positive association] between the {y_option} and the {x_option}")
elif cc >= 0.75:
    st.markdown(f"##### The correlation coefficient is :green[{cc}], which indicates a :green[strong positive association] between the {y_option} and the {x_option}")
elif cc >= 0.3:
    st.markdown(f"##### The correlation coefficient is :orange[{cc}], which indicates a :orange[weak positive association] between the {y_option} and the {x_option}")
elif cc >= -0.3:
    st.markdown(f"##### The correlation coefficient is :orange[{cc}], which indicates :yellow[no association] between the {y_option} and the {x_option}")
elif cc >= -0.75:
    st.markdown(f"##### The correlation coefficient is :red[{cc}], which indicates a :orange[weak negative association] between the {y_option} and the {x_option}")
elif cc >= -0.9:
    st.markdown(f"##### The correlation coefficient is :red[{cc}], which indicates a :red[strong negative association] between the {y_option} and the {x_option}")
elif cc > -1.0:
    st.markdown(f"##### The correlation coefficient is :red[{cc}], which indicates a :red[very strong negative association] between the {y_option} and the {x_option}")
elif cc == -1.0:
    st.markdown(f"##### The correlation coefficient is :red[{cc}], which indicates a :red[perfect negative association] between the {y_option} and the {x_option}")


fig = px.scatter(data_frame=df_scatter, x=x_option, y=y_option, color="DistrictName", size="number of residents",
                 color_continuous_scale="Reds")

st.plotly_chart(fig)

