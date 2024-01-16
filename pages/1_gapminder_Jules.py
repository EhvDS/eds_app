# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Read datasaets
df_num_houses = pd.read_csv('data/timed_data-NumberHouses.csv', delimiter=';')
df_population = pd.read_csv('data/timed_data-Population.csv', delimiter=';')

# Cleaning and preprocessing the data
# Renaming NbName to Neighborhood column for clarity
df_num_houses.rename(columns={'NbName': 'Neighborhood'}, inplace=True)
df_population.rename(columns={'NbName': 'Neighborhood'}, inplace=True)

# Melting the datasets
houses_long = df_num_houses.melt(id_vars='Neighborhood', var_name='Year', value_name='NumberHouses')
population_long = df_population.melt(id_vars='Neighborhood', var_name='Year', value_name='Population')

# Extracting year from the 'Year' column
houses_long['Year'] = houses_long['Year'].str.extract('(\d+)', expand=False)
population_long['Year'] = population_long['Year'].str.extract('(\d+)', expand=False)

# Converting the 'Year' column to integer as it is a numeric value
houses_long['Year'] = houses_long['Year'].astype(int)
population_long['Year'] = population_long['Year'].astype(int)

# Merging the datasets on Neighborhood and Year
merged_data = pd.merge(houses_long, population_long, on=['Neighborhood', 'Year'])

# Converting 'NumberHouses' and 'Population' to numeric values
merged_data['NumberHouses'] = pd.to_numeric(merged_data['NumberHouses'], errors='coerce')
merged_data['Population'] = pd.to_numeric(merged_data['Population'], errors='coerce')

# Creating the scatter plot
fig, ax = plt.subplots()
plt.title('Eindhoven Neighborhoods: Number of Houses vs Population Over Time')
plt.xlabel('Number of Houses')
plt.ylabel('Population')

# List of years in the dataset
years = merged_data['Year'].unique()

# Function to update the scatter plot for each year
def update(year):
    ax.clear()
    year_data = merged_data[merged_data['Year'] == year]
    scatter = ax.scatter(year_data['NumberHouses'], year_data['Population'], color='blue')
    plt.title(f'Eindhoven Neighborhoods: Number of Houses vs Population ({year})')
    plt.xlabel('Number of Houses')
    plt.ylabel('Population')
    plt.grid(True)

# Creating the animation
animation = FuncAnimation(fig, update, frames=years, repeat=True, interval=1000)

# Display the animation
plt.show()
