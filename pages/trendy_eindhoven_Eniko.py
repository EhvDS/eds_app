import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('./data/trendy_eindhoven_data_Eniko.csv')
st.write("# Explore trends in Eindhoven")

variable = st.selectbox("Select a variable:", ['Aantal woningen', 'Inwoners', 'Gemiddeld elektriciteitsverbruik totaal', 'Verplaatst zich meestal per fiets %',
                                              'Personenauto\'s totaal', 'Doet aan vrijwilligerswerk', 'Sport wekelijks (18-84 jaar)', 
                                              'Bezoekt culturele voorstellingen %', 'Registraties overlast per 1.000 inwoners',
                                              'Voelt zich wel eens onveilig in de eigen buurt %', 'Gemiddeld persoonlijk inkomen per inkomensontvanger (x1000 euro)',
                                              'Totaal aantal winkelpanden'])
size_ref = 1
if variable == 'Aantal woningen' or variable == 'Inwoners' or variable == 'Personenauto\'s totaal':
    size_ref = 500
elif  variable == 'Gemiddeld elektriciteitsverbruik totaal':
    size_ref = 100
    df = df[df['Gemiddeld elektriciteitsverbruik totaal'] != 0]
elif variable == 'Bezoekt culturele voorstellingen %':
    size_ref = 2
elif variable == 'Totaal aantal winkelpanden':
    size_ref = 5

figLine = px.line(df, x='year', y=variable, title=variable + '  per year per neighborhood:', color='neighborhood')
figLine.update_xaxes(type='category')

st.plotly_chart(figLine)

fig = px.scatter_mapbox(
    df,
    lat='latitude',
    lon='longitude',
    color='neighborhood',
    size=variable,
    hover_name='neighborhood',
    animation_frame='year',
    animation_group='neighborhood',
    mapbox_style='carto-positron',
    zoom=10,
).update_traces(marker=dict(sizemode='diameter', sizeref=size_ref))
frames = []
for year in df['year'].unique():
    frame_data = df[df['year'] == year]
    frame = px.scatter_mapbox(
        frame_data,
        lat='latitude',
        lon='longitude',
        color='neighborhood',
        size=variable,
        hover_name='neighborhood',
        mapbox_style='carto-positron',
        zoom=10,
    ).update_traces(marker=dict(sizemode='diameter', sizeref=size_ref))

    frames.append(go.Frame(data=frame.data, name=str(year)))

fig.frames = frames
st.write("Click play to see changes throughout the years:")
st.plotly_chart(fig)


