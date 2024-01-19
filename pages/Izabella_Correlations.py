import streamlit as st
import plotly.express as px
import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np
import sklearn as sk
import matplotlib
from numpy import mean
from numpy import std
import plotly.express as px
from numpy.random import randn
from numpy.random import seed
from matplotlib import pyplot
# from IPython.display import display
# from scipy import stats

st.write('# Correlations in Eindhoven')
st.markdown("*Made by Izabella Bogdanova*.")

st.caption('# What is correlation?')
st.markdown('Correlation coefficients quantify the association between variables or features of a dataset.')

st.image('https://files.realpython.com/media/py-corr-1.d13ed60a9b91.png')

st.markdown('Each of these plots shows one of three different forms of correlation:')
st.markdown('1. Negative correlation (red dots): In the plot on the left, the y values tend to decrease as the x values increase. This shows strong negative correlation, which occurs when large values of one feature correspond to small values of the other, and vice versa.')
st.markdown('2. Weak or no correlation (green dots): The plot in the middle shows no obvious trend. This is a form of weak correlation, which occurs when an association between two features is not obvious or is hardly observable.')
st.markdown('3. Positive correlation (blue dots): In the plot on the right, the y values tend to increase as the x values increase. This illustrates strong positive correlation, which occurs when large values of one feature correspond to large values of the other, and vice versa.')

df = pd.read_csv('./data/mostrecent_data_Izabella.csv')

st.markdown('Down below, you can find heatmap of all correlations. To see better, use zoom function on the plot.')

cols = ['number of residents', 'ScoreDiversity', 'NumberHouseholds',
       'AvgHouseValue', 'PctComplainsAQ', 'PctComplainsNoise',
       'AvgElectricityUsage', 'PctUnhappy', 'PctHighEducation',
       'PctLowEducation', 'PctFeelsUnsafe', 'ScoreSocialCohesion',
       'ScoreGoodLife', 'PctUnemployed', 'PctEconomicallyIndependent',
       'AvgIncome', 'NumberShops', 'Distance2Childcare',
       'Distance2Trainstation', 'Distance2HighwayEntrypoint',
       'Distance2FamilyDoctor', 'Distance2Cinema', 'Distance2Cafe',
       'Distance2SwimmingPool']
cm = np.corrcoef(df[cols].values, rowvar=0).round(decimals=2)
fig = px.imshow(cm, text_auto = True,
                color_continuous_scale = 'RdYlBu', 
                x = cols, 
                y = cols, 
                aspect="auto",
                title="Correlation Matrix")

# Plot!
st.plotly_chart(fig)

st.header('Demographic and Housing Correlations')
st.subheader('Correlation between "number of residents" and "number of households.')

code = df['number of residents'].corr(df['NumberHouseholds']).round(decimals=2)
st.text(code)
st.markdown('Here we have a correlation 0.96, hence I am going to show it.')

fig = px.scatter(df,
x="number of residents",
y="NumberHouseholds",
color = 'NbName',
title="Number of Residents VS Number Households with Neighbourhood name")
# Plot!
st.plotly_chart(fig)

fig = px.scatter(df,
x="number of residents",
y="NumberHouseholds",
trendline="ols",
trendline_color_override="red",
title="Number of Residents VS Number Households")
# Plot!
st.plotly_chart(fig)
st.markdown('In most cases, the number of residents in an area is closely related to the number of households. Each household typically represents a living unit, and the number of residents is the total population in those living units.')


st.header('Socioeconomic Correlations')
st.subheader('Relationship between the percentage of economically independent residents and the average income.')

code = df['PctEconomicallyIndependent'].corr(df['AvgIncome']).round(decimals=2)
st.text(code)

fig = px.scatter(df,
x="PctEconomicallyIndependent",
y="AvgIncome",
color = 'NbName',
title="PctEconomicallyIndependent VS AvgIncome with Neighbourhood name")
# Plot!
st.plotly_chart(fig)

fig = px.scatter(df,
x="PctEconomicallyIndependent",
y="AvgIncome",
trendline="ols",
trendline_color_override="red",
title="PctEconomicallyIndependent VS AvgIncome")
# Plot!
st.plotly_chart(fig)
st.markdown('This shows us a strong positive correlation, if a higher percentage of residents are economically independent, it is likely that the average income in the area would also be higher.')

st.header('Safety and Security Correlations')
st.subheader('Correlation between the percentage of residents feeling unsafe and the number of complaints related to noise.')

code = df['PctFeelsUnsafe'].corr(df['PctComplainsNoise']).round(decimals=2)
st.text(code)
st.markdown('We have a correlation between percentage of residents feeling unsafe and the number of complaints related to noise of 0.60.')

fig = px.scatter(df,
x="PctFeelsUnsafe",
y="PctComplainsNoise",
color = 'NbName',
title="PctFeelsUnsafe VS PctComplainsNoise with Neighbourhood name")
# Plot!
st.plotly_chart(fig)
fig = px.scatter(df,
x="PctFeelsUnsafe",
y="PctComplainsNoise",
trendline="ols",
trendline_color_override="red",
title="PctFeelsUnsafe VS PctComplainsNoise")
# Plot!
st.plotly_chart(fig)
st.markdown('The correlation might indicate that areas with more noise complaints tend to have residents who feel less safe, as both factors contribute to a less desirable living environment.')


st.subheader('Relationship between the perceived social cohesion score and the percentage of residents feeling unhappy')

code = df['ScoreSocialCohesion'].corr(df['PctUnhappy']).round(decimals=2)
st.text(code)
st.markdown('The correlation between the perceived social cohesion score and the percentage of residents feeling unhappy is moderately strong (0.66). This implies that areas with higher perceived social cohesion scores are associated with a lower percentage of residents feeling unhappy.')

fig = px.scatter(df,
x="ScoreSocialCohesion",
y="PctUnhappy",
color = 'NbName',
title="ScoreSocialCohesion VS PctUnhappy with Neighbourhood name")
# Plot!
st.plotly_chart(fig)

fig = px.scatter(df,
x="ScoreSocialCohesion",
y="PctUnhappy",
trendline="ols",
trendline_color_override="red",
title="ScoreSocialCohesion VS PctUnhappy")
# Plot!
st.plotly_chart(fig)
st.markdown('It could be argued that social isolation or lack of community support may be more common in neighbourhoods where residents feel that social cohesion is lower. This may contribute to feelings of unhappiness among residents. Also, datapoints here distributed only on right side.')


st.header('Education and Economic Factors')
st.subheader('Correlation between the percentage of high education and the average income.')

code = df['PctHighEducation'].corr(df['AvgIncome']).round(decimals=2)
st.text(code)
st.markdown('A correlation coefficient of 0.69 between the percentage of high education and average income suggests a moderately strong positive linear relationship between these two variables.')

fig = px.scatter(df,
x="PctHighEducation",
y="AvgIncome",
color = 'NbName',
title="PctHighEducation VS AvgIncome with Neighbourhood name")
# Plot!
st.plotly_chart(fig)


fig = px.scatter(df,
x="PctHighEducation",
y="AvgIncome",
trendline="ols",
trendline_color_override="red",
title="PctHighEducation VS AvgIncome")
# Plot!
st.plotly_chart(fig)
st.markdown('The correlation may reflect the reality that individuals with higher levels of education tend to earn higher incomes. Higher education levels often lead to greater skill sets and qualifications, making individuals more competitive in the job market and potentially resulting in higher-paying positions.')



st.subheader('Relationship between the percentage of high education and the percentage of economically independent residents.')

code = df['PctHighEducation'].corr(df['PctEconomicallyIndependent']).round(decimals=2)
st.text(code)

st.markdown('A correlation coefficient of 0.72 between the percentage of high education and the percentage of economically independent residents indicates a strong positive linear relationship between these two variables.')

fig = px.scatter(df,
x="PctHighEducation",
y="PctEconomicallyIndependent",
color = 'NbName',
title="PctHighEducation VS PctEconomicallyIndependent with Neighbourhood name")
# Plot!
st.plotly_chart(fig)

fig = px.scatter(df,
x="PctHighEducation",
y="PctEconomicallyIndependent",
trendline="ols",
trendline_color_override="red",
title="PctHighEducation VS PctEconomicallyIndependent")
# Plot!
st.plotly_chart(fig)
st.markdown('Individuals with higher levels of education often acquire skills and qualifications that make them more employable and better positioned for economic independence. The positive correlation could reflect the notion that a community with a higher percentage of highly educated individuals also has a higher percentage of economically independent residents.')



st.header('Health and Environment Correlations')
st.subheader('Correlation between the percentage of complaints related to air quality and noise.')

code = df['PctComplainsAQ'].corr(df['PctComplainsNoise']).round(decimals=2)
st.text(code)
st.markdown('A correlation coefficient of 0.88 between the percentage of complaints related to air quality and noise indicates a very strong positive linear relationship between these two variables.')

fig = px.scatter(df,
x="PctComplainsAQ",
y="PctComplainsNoise",
color = "NbName",
title="PctComplainsAQ VS PctComplainsNoise with Neighbourhood name")
# Plot!
st.plotly_chart(fig)

fig = px.scatter(df,
x="PctComplainsAQ",
y="PctComplainsNoise",
trendline="ols",
trendline_color_override="red",
title="PctComplainsAQ VS PctComplainsNoise")
# Plot!
st.plotly_chart(fig)

st.markdown('Both air quality and noise complaints may be influenced by shared environmental factors. For example, industrial activities, traffic, or construction projects can contribute to both poor air quality and increased noise levels in a given area.')


st.header('Accessibility and Distance Correlations')
st.subheader('Correlation between "Distance2Trainstation" and "Distance2Cinema.')

code = df['Distance2Trainstation'].corr(df['Distance2Cinema']).round(decimals=2)
st.text(code)
st.markdown('A correlation coefficient of 0.87 between "Distance2Trainstation" and "Distance2Cinema" indicates a very strong positive linear relationship between these two variables.')

fig = px.scatter(df,
x="Distance2Trainstation",
y="Distance2Cinema",
color = "NbName",
title="Distance2Trainstation VS Distance2Cinema with Neighbourhood name")
# Plot!
st.plotly_chart(fig)

fig = px.scatter(df,
x="Distance2Trainstation",
y="Distance2Cinema",
trendline="ols",
trendline_color_override="red",
title="Distance2Trainstation VS Distance2Cinema")
# Plot!
st.plotly_chart(fig)
st.markdown('Train stations and cinemas are often located in urban or central areas. This dataset includes neighborhoods in urban environments, the correlation reflects the tendency for both train stations and cinemas to be situated close to central locations.')
































