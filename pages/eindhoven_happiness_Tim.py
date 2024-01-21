import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

plt.rcParams['text.color'] = 'black'
plt.rcParams['axes.labelcolor'] = 'black'
plt.rcParams['xtick.color'] = 'black'
plt.rcParams['ytick.color'] = 'black'

st.set_page_config(layout="wide")
# Function to create the Plotly map with GeoJSON
def create_map(df):
    # Assuming 'Geoshape' column contains stringified GeoJSON and 'NbName' is the identifier
    features = []
    for _, row in df.iterrows():
        geoshape_json = json.loads(row["Geoshape"])
        geoshape = {'type': 'Feature',
            'properties': {'name': row['Neighbourhood']},
            'id': row["NbId"],
            'geometry': geoshape_json}
        features.append(geoshape)
        if len(features) <= 5:
            print(geoshape)
    geojson = {'type': 'FeatureCollection', 'features': features}
    # Create a DataFrame for the locations
    color_scale = [
    (0, "grey"),  # Color for 0 values
    # Define other colors for the rest of your scale
    (0.72, "red"),  # Example: Color for values > 0
    (0.88, "white"),
    (1, "green") # Ensure the scale covers the full range of your data
    ]
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        color='Happiness score',
        color_continuous_scale=color_scale,
        locations="NbId",
        featureidkey="id",
        center={"lat": 51.4416, "lon": 5.4697},
        hover_data=['Neighbourhood', 'Happiness', "Happiness rank", "Happiness score"], # Adjust as needed
        mapbox_style="open-street-map",
        zoom=11.5,
        opacity=0.8
    )
    
    fig.update_layout(
        height=950,  # Set the height of the map in pixels
        width=950    # Set the width of the map in pixels
    )
    fig.update_traces(
    hoverlabel=dict(font_size=15)  
    # Adjust the font size as needed
    )

    return fig

# Streamlit app
def app():
    st.title('Happiness in Eindhoven Neighbourhoods')

    # Load your dataset
    df = pd.read_csv("data/tim_main_dataset.csv")  # Replace with your actual file path and name
    df_top_30 = df.head(30)
    value_counts = df_top_30['Preferrable type of transport'].value_counts()
    st_map = create_map(df)
    st.plotly_chart(st_map, use_container_width=True)
    
    st.markdown("### Preferrable transport type of top-30 happiest Eindhoven districts")
    fig, ax = plt.subplots(figsize=(6, 6))
    explode = (0, 0.1, 0, 0)
    colors = ['#7792bd','#e1e9f5','#2f4f82','#062454']
    
    # Create a pie chart on the axis
    ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', explode=explode, shadow=True, startangle=90, colors = colors)
    # Display the plot in Streamlit
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)
    
    st.markdown("### Percentage of people doing sports vs. Happiness score")
    fig1, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(df["Happiness score"], df["PctSports"])
    
    ax.set_xlabel('Happiness Score')  # Set x-axis label
    ax.set_ylabel("% of people engaged in sports")
    ax.set_title('Happiness Score vs Physical activity')
    buf = BytesIO()
    fig1.savefig(buf, format="png")
    st.image(buf)
    smileys_replaced = df
    smileys_replaced["Happiness rank"] = smileys_replaced["Happiness rank"].replace("🥉", 3)
    smileys_replaced["Happiness rank"] = smileys_replaced["Happiness rank"].replace("🥈", 2)
    smileys_replaced["Happiness rank"] = smileys_replaced["Happiness rank"].replace("🥇", 1)
    smileys_replaced["PctUnemployed"] = smileys_replaced["PctUnemployed"].replace("N/A", pd.NA)
    smileys_replaced["PctHighEducation"] = smileys_replaced["PctHighEducation"].replace("N/A", pd.NA)
    smileys_replaced["Happiness rank"] = pd.to_numeric(smileys_replaced["Happiness rank"], errors="coerce")
    smileys_replaced = smileys_replaced.dropna(subset=["Happiness rank"])
    smileys_replaced = smileys_replaced.dropna(subset=["PctHighEducation"])
    smileys_replaced = smileys_replaced.dropna(subset=["PctUnemployed"])
    smileys_replaced = smileys_replaced.sort_values(by='Happiness rank', ascending=True)

    st.markdown("### How higher education and unemployment influences happiness")
    fig2, ax = plt.subplots(figsize=(8, 6))
    ax.plot(smileys_replaced['Happiness rank'], smileys_replaced["PctHighEducation"], label="% of people with higher education")
    ax.plot(smileys_replaced['Happiness rank'], smileys_replaced["PctUnemployed"], label="% of unemployed")
    ax.set_xlabel('The unhappiest                                Happiness rank                              The happiest')
    ax.set_ylabel('Values')

# Flip the x-axis
    ax.set_xlim(max(df['Happiness rank']), min(df['Happiness rank']))
    ax.legend()
    buf = BytesIO()
    fig2.savefig(buf, format="png")
    st.image(buf)
    # Show the plot
    st.markdown("#### Conclusion (as it may seem unclear from the graph): higher education and employment = more happiness")
    st.markdown("### How average age correlates with happiness")

    bins = [0, 10, 25, 40, 55, 70, 92]
    labels = ['Top 10', 'Top 10-25', 'Top 25-40', 'Top 40-55', 'Bottom 55-70', 'Bottom 70-92']

    # Create a new column 'Group' based on these bins
    smileys_replaced['Group'] = pd.cut(smileys_replaced['Happiness rank'], bins=bins, labels=labels, right=False)

    # Calculate the average age for each group
    grouped_avg_age = smileys_replaced.groupby('Group')['average age'].mean().reindex(labels)
    fig3, ax = plt.subplots(figsize=(9, 7))
    colors = ['#46874b', '#76b37a', '#a9ccac', '#dea0a0', '#d46868', '#9c3333']

    grouped_avg_age.plot(kind='bar', ax=ax, color=colors)

    # Set the title and labels
    ax.set_title('Average age of a neighbourhood vs happiness rank')
    ax.set_xlabel('Happiness Rank Group')
    ax.set_ylabel('Average Age (years)')

    # Rotate x-tick labels for better readability
    plt.xticks(rotation=45, ha='right')
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    # Adjust the y-axis range
    ax.set_ylim(30, 46)

    # Show the plot in Streamlit
    buf = BytesIO()
    fig3.savefig(buf, format="png")
    st.image(buf)
    
app()
