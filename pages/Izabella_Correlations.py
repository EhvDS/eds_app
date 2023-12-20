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
                x = df.columns, 
                y = df.columns, 
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

fig = px.scatter(df,
x="PctFeelsUnsafe",
y="PctComplainsNoise",
title="PctFeelsUnsafe VS PctComplainsNoise")
# Plot!
st.plotly_chart(fig)
st.markdown('We have a correlation between percentage of residents feeling unsafe and the number of complaints related to noise of 0.60.')
st.markdown('The correlation might indicate that areas with more noise complaints tend to have residents who feel less safe, as both factors contribute to a less desirable living environment.')

fig = px.scatter(df,
x="PctFeelsUnsafe",
y="PctComplainsNoise",
trendline="ols",
trendline_color_override="red",
title="PctFeelsUnsafe VS PctComplainsNoise")
# Plot!
st.plotly_chart(fig)

st.subheader('Relationship between the perceived social cohesion score and the percentage of residents feeling unhappy')

code = df['ScoreSocialCohesion'].corr(df['PctUnhappy']).round(decimals=2)
st.text(code)

fig = px.scatter(df,
x="ScoreSocialCohesion",
y="PctUnhappy",
title="ScoreSocialCohesion VS PctUnhappy")
# Plot!
st.plotly_chart(fig)
st.markdown('It could be argued that social isolation or lack of community support may be more common in neighbourhoods where residents feel that social cohesion is lower. This may contribute to feelings of unhappiness among residents. Also, datapoints here distributed only on right side.')

fig = px.scatter(df,
x="ScoreSocialCohesion",
y="PctUnhappy",
trendline="ols",
trendline_color_override="red",
title="ScoreSocialCohesion VS PctUnhappy")
# Plot!
st.plotly_chart(fig)


st.header('Education and Economic Factors')
st.subheader('Correlation between the percentage of high education and the average income.')

code = df['PctHighEducation'].corr(df['AvgIncome']).round(decimals=2)
st.text(code)

st.markdown('The correlation may reflect the reality that individuals with higher levels of education tend to earn higher incomes.')

fig = px.scatter(df,
x="PctHighEducation",
y="AvgIncome",
title="PctHighEducation VS AvgIncome")
# Plot!
st.plotly_chart(fig)
st.markdown('Higher education levels often lead to greater skill sets and qualifications, making individuals more competitive in the job market and potentially resulting in higher-paying positions.')

fig = px.scatter(df,
x="PctHighEducation",
y="AvgIncome",
trendline="ols",
trendline_color_override="red",
title="PctHighEducation VS AvgIncome")
# Plot!
st.plotly_chart(fig)







































