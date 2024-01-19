# importing libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import statsmodels.api as sm

# Loading gender and age data
@st.cache_data
def load_gender_age_data():
    df = pd.read_csv('./data/dataset-iris-part-1.csv')

    # Splitting the column names into separate columns for 'Category' and 'Year'
    df_melted = df.melt(id_vars=['NbName', 'DistrictId', 'DistrictName'], var_name='CategoryYear', value_name='Population')
    df_melted['Year'] = df_melted['CategoryYear'].apply(lambda x: int(x.split('|')[1]) if '|' in x and x.split('|')[1].isdigit() else None)
    df_melted['Category'] = df_melted['CategoryYear'].apply(lambda x: x.split('|')[0] if '|' in x else None)

    # Converting the 'Population' column to numeric values
    df_melted['Population'] = pd.to_numeric(df_melted['Population'], errors='coerce')

    # Dropping rows with missing values in the 'Year', 'Category', and 'Population' columns
    df_melted.dropna(subset=['Year', 'Category', 'Population'], inplace=True)
    df_melted.drop('CategoryYear', axis=1, inplace=True)
    return df_melted

# Loading population pyramid data
def pyramid_data():
    df_pyramid = pd.read_csv('./data/dataset-iris-part-2.csv', sep=';', encoding='utf-8')
    return df_pyramid

# This function plots the population of gender over time for the selected neighborhoods
def select_and_plot(df, category, title):
    # Adding a multiselect functionality to choose the neighborhoods
    neighborhoods = sorted(df['NbName'].unique(), key=lambda x: x.lstrip("'t ").lower())
    selected_neighborhoods = st.multiselect('Select neighborhood(s):', neighborhoods, default=neighborhoods[:0])
    filtered_data = df[df['NbName'].isin(selected_neighborhoods) & (df['Category'] == category)]

    # Calculating the overall average for the selected category, so that an average line can be added to the plot
    overall_avg = df[df['Category'] == category].groupby('Year')['Population'].mean().reset_index()
    overall_avg['NbName'] = 'Overall Average'
    fig = px.line(filtered_data, x='Year', y='Population', color='DistrictName', line_group='NbName', title=f'{title} by neighborhood')
    fig.update_layout(legend_title_text='Neighborhoods')
    fig.add_scatter(x=overall_avg['Year'], y=overall_avg['Population'], mode='lines', name='Overall Average', line=dict(dash='dot', color='black'))
    st.plotly_chart(fig)

# This function plots the population of gender over time for the selected neighborhoods, for the 'All' option
def select_and_plot_all_genders(df):
    neighborhoods = sorted(df['NbName'].unique(), key=lambda x: x.lstrip("'t ").lower())
    selected_neighborhood = st.selectbox('Select a neighborhood to compare:', neighborhoods)

    # Filtering data for selected neighborhoods
    filtered_data = df[(df['NbName'] == selected_neighborhood) & (df['Category'].isin(['Mannen', 'Vrouwen']))]
    # Creating the custom colors for the plot
    custom_colors = {'Mannen': '#CC112F', 'Vrouwen': '#117acc'}
    
    # Scatter plot with trend lines to visualize trends
    fig = px.scatter(filtered_data, x='Year', y='Population', color='Category', facet_col='NbName', trendline='ols',        
                     color_discrete_map=custom_colors, 
                     labels={'Category': 'Gender', 'NbName': 'Neighborhood'}, title='Gender trends across neighborhoods')

    fig.update_layout(legend_title_text='Gender')
    st.plotly_chart(fig)

# This function plots the population over time for the selected neighborhoods, for the ages option
def plot_all_age_groups(df):
    years = sorted(df['Year'].unique())
    for year in years:
        df_year = df[df['Year'] == year]
        age_categories = ['Totaal 0-9 jaar', 'Totaal 10-19 jaar', 'Totaal 20-29 jaar', 'Totaal 30-39 jaar', 'Totaal 40-49 jaar', 'Totaal 50-59 jaar', 'Totaal 60-69 jaar', 'Totaal 70-79 jaar', 'Totaal 80-89 jaar', 'Totaal 90 jaar en ouder']
        df_plot = df_year[df_year['Category'].isin(age_categories)]
        fig = px.pie(df_plot, names='Category', values='Population', title=f'Population distribution in {year}')
        st.plotly_chart(fig)

# Define a function for the population pyramid visualization
def population_pyramid(df):
    # Create a selectbox to choose the neighborhood
    neighborhood = st.selectbox("Select neighborhood", df["Buurten"].unique())

    # Extracting unique years from the column names
    years = sorted(set(col.split("|")[2] for col in df.columns if col.startswith("Inwoners naar kenmerken|")))

    # Creating a selectbox to choose the year
    year = st.slider("Select year", min_value=2015, max_value=2021, value=2015, step=1)

    # Defining the age groups
    age_group_labels = ["0-9 jaar", "10-19 jaar", "20-29 jaar", "30-39 jaar", "40-49 jaar", "50-59 jaar", "60-69 jaar", "70-79 jaar", "80-89 jaar", "90+ jaar"]

    # Replacing 'x' with NaN in the population columns
    for label in age_group_labels:
        male_column = f"Inwoners naar kenmerken|{label}|{year}|Man"
        female_column = f"Inwoners naar kenmerken|{label}|{year}|Vrouw"
        df[male_column] = pd.to_numeric(df[male_column], errors='coerce')
        df[female_column] = pd.to_numeric(df[female_column], errors='coerce')

    # Filtering data for the selected neighborhood and year
    filtered_df = df[(df["Buurten"] == neighborhood)]

    # Creating the population pyramid data
    y = age_group_labels

    # Filtering out NaN values in the population columns, and converting the values to integers. x2 is multiplied by -1 to add the values on the left side of the pyramid
    x1 = filtered_df[[f"Inwoners naar kenmerken|{label}|{year}|Man" for label in age_group_labels]].astype(float).values.flatten()
    x2 = filtered_df[[f"Inwoners naar kenmerken|{label}|{year}|Vrouw" for label in age_group_labels]].astype(float).values.flatten() * -1

    # Calculating the tickvals and ticktext for the x-axis based on the data range
    valid_values = [val for val in x1 if not np.isnan(val)] + [val for val in x2 if not np.isnan(val)]

    # Calculating the tickvals and ticktext for the x-axis based on the data range
    if valid_values:
        min_value = min(valid_values)
        max_value = max(valid_values)
        tick_step = 200
        tickvals = list(range(int(min_value), int(max_value) + tick_step, tick_step))
        ticktext = [str(abs(val)) if val != 0 else '0' for val in tickvals] 
    else:
        # Handling the case when there are no valid values
        min_value = 0
        max_value = 1000
        tick_step = 200
        tickvals = list(range(int(min_value), int(max_value) + tick_step, tick_step))
        ticktext = [str(abs(val)) if val != 0 else '0' for val in tickvals]


    # Creating an instance of the figure
    fig = go.Figure()

    # Adding Male and Female traces to the figure
    fig.add_trace(go.Bar(
        y=y,
        x=x1,
        name='Male',
        orientation='h',
        marker=dict(color='#CC112F')
    ))

    fig.add_trace(go.Bar(
        y=y,
        x=x2,
        name='Female',
        orientation='h', 
        marker=dict(color='#117acc')
    ))

    # Updating Figure Layout
    fig.update_layout(
        template='plotly_white',
        title=f'Population pyramid for {neighborhood} in {year}',
        title_font_size=24,
        barmode='relative',
        bargap=0.0,
        bargroupgap=0,
        xaxis=dict(
            tickvals=tickvals,
            ticktext=ticktext,        
            title='Population',
            title_font_size=14
        )
    )

    # Plotting the figure
    st.plotly_chart(fig)

# In the main function, all functions are called and we create the layout of the app. We have a title, a description and selectbox to choose which category will be visualized. 
def main():
    st.title('Trends in Eindhoven 📈')
    df_gender_age  = load_gender_age_data()

    # After the option is selected, the corresponding function is called
    choose_category = st.selectbox('Choose category:', ['Gender', 'Age', 'Population pyramid'])
    if choose_category == 'Gender':
        st.write('Here you can see the population trends for the selected neighborhoods. You can choose to look at both genders or at just one of them. If you select either Mannen or Vrouwen, you will see a scatter plot with trend lines. You can select one or multiple neighborhood(s) in the dropdown menu. Hover over the graph to see the exact values.') 
        st.caption('The data was collected from: https://eindhoven.incijfers.nl/jive.')
        choose_gender = st.selectbox('Choose gender:', ['All', 'Mannen', 'Vrouwen'])
        if choose_gender == 'All':
            select_and_plot_all_genders(df_gender_age)
        elif choose_gender == 'Mannen':
            select_and_plot(df_gender_age, 'Mannen', 'Mannen trends')
        elif choose_gender == 'Vrouwen':
            select_and_plot(df_gender_age, 'Vrouwen', 'Vrouwen trends')
    elif choose_category == 'Age':
        st.write('Here you can see the population distribution for the selected neighborhoods. You can choose to look at all age groups or at one of them. If you select one of the age groups, you will see a pie chart with the population distribution for that age group. You can select one or multiple neighborhood(s) in the dropdown menu. Hover over the graph to see the exact values.')
        st.caption('The data was collected from: https://eindhoven.incijfers.nl/jive.')
        age_groups = ['All', 'Totaal 0-9 jaar', 'Totaal 10-19 jaar', 'Totaal 20-29 jaar', 'Totaal 30-39 jaar', 'Totaal 40-49 jaar', 'Totaal 50-59 jaar', 'Totaal 60-69 jaar', 'Totaal 70-79 jaar', 'Totaal 80-89 jaar', 'Totaal 90 jaar en ouder']
        choose_age_group = st.selectbox('Choose age group:', age_groups)
        if choose_age_group == 'All':
            plot_all_age_groups(df_gender_age)
        else:
            select_and_plot(df_gender_age, choose_age_group, f'Population trends for {choose_age_group}')
    elif choose_category == 'Population pyramid':
        st.write('Here you can see the population pyramid for the selected neighborhood and year. You can see the population distribution for each age group. Select a neighborhood in the dropdown menu and a year using the slider. Hover over the graph to see the exact values.')
        st.caption('This visualization is not available for all neighborhoods. If the plot is empty, it means there was no data for that neighborhood. The data was collected from: https://eindhoven.incijfers.nl/jive.')
        df_pyramid = pyramid_data()
        population_pyramid(df_pyramid)

if __name__ == "__main__":
    main()