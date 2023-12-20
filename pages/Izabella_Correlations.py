import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import seaborn as sns
import numpy as np
import pandas as pd
import sklearn as sk
import matplotlib
import matplotlib.pyplot as plt
from numpy import mean
from numpy import std
import plotly.express as px
from numpy.random import randn
from numpy.random import seed
from matplotlib import pyplot
from IPython.display import display
from scipy import stats

st.write('# Correlations in Eindhoven')

st.caption('# What is correlation?')
st.text('Correlation coefficients quantify the association between variables or features of a dataset.')

st.image('https://files.realpython.com/media/py-corr-1.d13ed60a9b91.png')

st.text('Each of these plots shows one of three different forms of correlation:')
st.text('1. Negative correlation (red dots): In the plot on the left, the y values tend to decrease as the x values increase. This shows strong negative correlation, which occurs when large values of one feature correspond to small values of the other, and vice versa.')
st.text('2. Weak or no correlation (green dots): The plot in the middle shows no obvious trend. This is a form of weak correlation, which occurs when an association between two features is not obvious or is hardly observable.')
st.text('3. Positive correlation (blue dots): In the plot on the right, the y values tend to increase as the x values increase. This illustrates strong positive correlation, which occurs when large values of one feature correspond to large values of the other, and vice versa.')

df = pd.read_csv('./data/mostrecent_data_Izabella.csv')

st.text('Down below, you can find heatmap of all correlations. To see better, use zoom function on the plot.')

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
                x = df.columns, 
                y = df.columns, 
                aspect="auto")

# Plot!
st.plotly_chart(fig)

st.header('Demographic and Housing Correlations')
st.subheader('Correlation between "number of residents" and "number of households.')

code = df['number of residents'].corr(df['NumberHouseholds']).round(decimals=2)
st.text(code)
st.text('Here we have a correlation 0.96, hence I am going to show it.')

fig = px.scatter(df,
x="number of residents",
y="NumberHouseholds",
trendline="ols",
trendline_color_override="red",
title="Number of Residents VS Number Households")
# Plot!
st.plotly_chart(fig)
st.text('In most cases, the number of residents in an area is closely related to the number of households. Each household typically represents a living unit, and the number of residents is the total population in those living units.')


st.header('Socioeconomic Correlations')
st.subheader('Relationship between the percentage of economically independent residents and the average income.')

code = df['PctEconomicallyIndependent'].corr(df['AvgIncome']).round(decimals=2)
st.text(code)

fig = px.scatter(df,
x="PctEconomicallyIndependent",
y="AvgIncome",
trendline="ols",
trendline_color_override="red",
title="PctEconomicallyIndependent VS AvgIncome")
# Plot!
st.plotly_chart(fig)
st.text('This shows us a strong positive correlation, if a higher percentage of residents are economically independent, it is likely that the average income in the area would also be higher.')

st.header('Safety and Security Correlations')
st.subheader('Correlation between the percentage of residents feeling unsafe and the number of complaints related to noise.')









































