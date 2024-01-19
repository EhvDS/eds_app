import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import numpy as np
import matplotlib.lines as mlines
import mplcursors

# Global variable to store the cursor
cursor = None

# Read datasets
df_num_houses = pd.read_csv('data/timed_data-NumberHouses.csv', delimiter=';')
df_population = pd.read_csv('data/timed_data-Population.csv', delimiter=';')
df_health = pd.read_csv('data/timed_data-Health-bad-to-worst.csv', delimiter=';')
df_woz = pd.read_csv('data/timed_data-WOZ.csv', delimiter=';')

# Cleaning and preprocessing the data
df_num_houses.rename(columns={'NbName': 'Neighborhood'}, inplace=True)
df_population.rename(columns={'NbName': 'Neighborhood'}, inplace=True)
df_health.rename(columns={'Buurten': 'Neighborhood'}, inplace=True)
df_woz.rename(columns={'Buurten': 'Neighborhood'}, inplace=True)

# Melting the datasets
houses_long = df_num_houses.melt(id_vars='Neighborhood', var_name='Year', value_name='NumberHouses')
population_long = df_population.melt(id_vars='Neighborhood', var_name='Year', value_name='Population')
health_long = df_health.melt(id_vars='Neighborhood', var_name='Year', value_name='Health')
woz_long = df_woz.melt(id_vars='Neighborhood', var_name='Year', value_name='WOZ')

# Extracting year from the 'Year' column
houses_long['Year'] = houses_long['Year'].str.extract('(\d+)', expand=False)
population_long['Year'] = population_long['Year'].str.extract('(\d+)', expand=False)
health_long['Year'] = health_long['Year'].str.extract('(\d+)', expand=False)
# extract last 4 digits in year as woz_long has a different format
woz_long['Year'] = woz_long['Year'].str[-4:]


# Converting the 'Year' column to integer
houses_long['Year'] = houses_long['Year'].astype(int)
population_long['Year'] = population_long['Year'].astype(int)
health_long['Year'] = health_long['Year'].astype(int)
woz_long['Year'] = woz_long['Year'].astype(int)

# drop years outside of 2008-2021
houses_long = houses_long[(houses_long['Year'] >= 2008) & (houses_long['Year'] <= 2021)]
population_long = population_long[(population_long['Year'] >= 2008) & (population_long['Year'] <= 2021)]
health_long = health_long[(health_long['Year'] >= 2008) & (health_long['Year'] <= 2021)]
woz_long = woz_long[(woz_long['Year'] >= 2008) & (woz_long['Year'] <= 2021)]

# Merging the datasets on Neighborhood and Year
merged_data = pd.merge(houses_long, population_long, on=['Neighborhood', 'Year'])

# Converting 'NumberHouses' and 'Population' to numeric values
merged_data['NumberHouses'] = pd.to_numeric(merged_data['NumberHouses'], errors='coerce')
merged_data['Population'] = pd.to_numeric(merged_data['Population'], errors='coerce')
merged_data = pd.merge(merged_data, health_long, on=['Neighborhood', 'Year'])

# convert the 'Health' column to integer and fix NaN values
merged_data['Health'] = pd.to_numeric(merged_data['Health'], errors='coerce').fillna(0).astype(int)

merged_data = pd.merge(merged_data, woz_long, on=['Neighborhood', 'Year'])

# convert the 'WOZ' column to integer and fix NaN values
merged_data['WOZ'] = pd.to_numeric(merged_data['WOZ'], errors='coerce').fillna(0).astype(int)

# Creating the scatter plot
fig, ax = plt.subplots()
# set size of graph
fig.set_size_inches(15, 10)
plt.title('Eindhoven Neighborhoods: Number of Houses vs Population Over Time')
plt.xlabel('Number of Houses')
plt.ylabel('Population')

# List of years in the dataset
years = merged_data['Year'].unique()

# Determine limits for the axes to prevent moving during animation
x_min, x_max = merged_data['NumberHouses'].min(), merged_data['NumberHouses'].max() + 100
y_min, y_max = merged_data['Population'].min(), merged_data['Population'].max() + 1000

# Set the limits for the axes
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# Normalization function
def normalize(column):
    max_value = column.max()
    min_value = column.min()
    return (column - min_value) / (max_value - min_value)

# Apply normalization to the 'WOZ' column
merged_data['WOZ'] = pd.to_numeric(merged_data['WOZ'], errors='coerce').fillna(1)
merged_data['WOZ_normalized'] = normalize(merged_data['WOZ']) * 100  # Scale from 0 to 100

# Calculate the percentage of bad to worst health
merged_data['Health_Percentage'] = (merged_data['Health'] / merged_data['Population']) * 100
health_norm = merged_data['Health_Percentage']**0.3
health_norm = Normalize(vmin=health_norm.min(), vmax=health_norm.max())
# normalize the health percentage and round to 3 decimals
merged_data['Health_Percentage_Norm'] = (merged_data['Health_Percentage'] / merged_data['Population']) * 100
merged_data['Health_Percentage_Norm'] = merged_data['Health_Percentage_Norm'].round(3)


# Create a color map
cmap = cm.RdYlGn_r  # Red to Green reversed color map

# Define sizes for the WOZ legend
woz_sizes = [200, 400, 600]
# Define colors for the health legend (use the color map)
health_colors = cmap(np.linspace(0, 1, 4))
health_labels = ['Good', 'Medium', 'Bad', 'Worst']  # Labels for the health gradient

# health gradient
health_proxy = [mlines.Line2D([], [], color=color, marker='o', linestyle='None',
                             markersize=10, label=label) for color, label in zip(health_colors, health_labels)]

# Making space for legends
plt.subplots_adjust(right=0.8)

# Function to create legends
def create_legends(ax):
    # Legend for WOZ sizes
    woz_legend_elements = [plt.scatter([], [], s=custom_scale(size, 0.003), color='grey', alpha=0.6, label=label) 
                           for size, label in zip(woz_sizes, woz_sizes)]
    woz_legend = ax.legend(handles=woz_legend_elements, title='Average WOZ Value', loc='upper left', bbox_to_anchor=(1.05, 1))

    # Legend for Health Gradient
    health_legend = ax.legend(handles=health_proxy, title='Health Gradient', loc='lower left', bbox_to_anchor=(1.05, 0))

    # Add legends to the axes
    ax.add_artist(woz_legend)
    ax.add_artist(health_legend)

# Custom scaling function
def custom_scale(value, a=0.35):
    return (value ** 2) * a

# Function to update the scatter plot for each year
def update(year):
    global cursor
    ax.clear()
    year_data = merged_data[merged_data['Year'] == year]
    
    # Apply custom scaling function to normalized WOZ values
    sizes = custom_scale(year_data["WOZ_normalized"])
    
    # Calculate the normalized health percentage for the year
    health_percentage_norm = year_data['Health_Percentage']**0.5
    
    # Map the normalized health percentage to the color map
    colors = cmap(health_norm(health_percentage_norm))

    # Scatter plot for the actual data
    scatter = ax.scatter(year_data['NumberHouses'], year_data['Population'], s=sizes, c=colors, alpha=0.7)
    
    # Set titles and labels
    ax.set_title(f'Eindhoven Neighborhoods: Number of Houses vs Population ({year})')
    ax.set_xlabel('Number of Houses')
    ax.set_ylabel('Population')
    
    # Grid, axis limits, and watermark
    ax.grid(True)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # Create the legends
    create_legends(ax)

     # Remove previous annotations
    if cursor is not None:
        cursor.remove()

    # Add cursor that will show Neighborhood, Number of Houses, Population, Health, and WOZ on hover
    cursor = mplcursors.cursor(scatter, hover=True)
    cursor.connect(
        "add", lambda sel: sel.annotation.set_text(
            f'Neighborhood: {year_data.iloc[sel.target.index]["Neighborhood"]}\n'
            f'Number of Houses: {year_data.iloc[sel.target.index]["NumberHouses"]}\n'
            f'Population: {year_data.iloc[sel.target.index]["Population"]}\n'
            f'Bad/Worst Health in percentage: {year_data.iloc[sel.target.index]["Health_Percentage_Norm"]}%\n'
            f'Average WOZ worth: €{year_data.iloc[sel.target.index]["WOZ"]}.000,-'
        )
    )

# Initially create the legends
create_legends(ax)

# Creating the animation
ani = FuncAnimation(fig, update, frames=years, repeat=True, interval=4000)

plt.show()
