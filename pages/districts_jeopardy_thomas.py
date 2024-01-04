import pandas as pd
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import StrMethodFormatter
import numpy as np
from pandas import Series
import random


# Set the page layout to wide view, so that horizontal space is available on large screens
st.set_page_config(layout="wide", page_title="District Jeopardy", page_icon="🎓")

# Keys used to store states persistently
board_key = "thomas_jeopardy_board"
points_key = "thomas_jeopardy_points"
state_key = "thomas_jeopardy_state"
answers_key = "thomas_jeopardy_answers"
question_args_key = "thomas_jeopardy_question_args"
# Get the dataset that will be used throughout the questions
ndf = pd.read_csv("data/neighborhood_data_thomas.csv")
ddf = pd.read_csv("data/district_data_thomas.csv")

numeric_features = ["residents", "area", "stores"]

# Function to display the Jeopardy board
def display_jeopardy_board():
    board_df = st.session_state[board_key]
    
    # Create visual board rendering
    with st.container():
        district_columns = st.columns(len(board_df.columns), gap="small")
        for column_idx, column in enumerate(district_columns):
            # Single district column
            with column:
                with st.container(border=True):
                    district = board_df.columns[column_idx]
                    options = board_df.loc[:, district]
                    st.text(district)
                    for option in options:
                        # Single option within district cell
                        if st.button(f"${option['prize']}", key=f"{district}-{option['difficulty']}", use_container_width=True, disabled=option["completed"]):
                            # Button on click logic
                            # Store the selected option in the current state
                            st.session_state[state_key] = option
                            st.rerun() # Disgustingly re-render, to make sure the renderer is properly representing the changes made

def get_value_range(values: Series, operation, error_margin_percentage):
    if (operation == "highest"):
        correct_answer = values.max()
    elif (operation == "lowest"):
        correct_answer = values.min()
    elif (operation == "median"):
        correct_answer = values.median()
    median_range_anchor = values.median() # Base the range around correct answer on the median, as this will give a fair range for the entire range of possible values
    start_correct_range = correct_answer - (error_margin_percentage / 100)*median_range_anchor
    end_correct_range = correct_answer + (error_margin_percentage / 100)*median_range_anchor
    return start_correct_range, end_correct_range

def answer_classification_question(answer: Series):
    state = st.session_state[state_key]
    if (state is None):
        return # Just return if no valid state is set
    
    question_is_correct = answer["is_correct"]
    state["correct"] = question_is_correct 
    if (question_is_correct):
        # Answer was correct so give the points
        st.session_state[points_key] = st.session_state[points_key] + state["prize"]
    state["completed"] = True

def answer_open_question(answer: int, values: Series, operation, error_margin_percentage):
    state = st.session_state[state_key]
    if (state is None):
        return # Just return if no valid state is set
    
    start_correct_range, end_correct_range = get_value_range(values, operation, error_margin_percentage)
    question_is_correct = start_correct_range <= answer <= end_correct_range
    state["correct"] = question_is_correct 
    if (question_is_correct):
        # Answer was correct so give the points
        st.session_state[points_key] = st.session_state[points_key] + state["prize"]
    state["completed"] = True

def display_question(header: DeltaGenerator):
    # executable question, have it in the question display as we are not allowed to split the python file in multiple files
    def numeric_classification_question(district, feature, higher_operator):
        feature_string = f"area in m\N{SUPERSCRIPT TWO}" if feature == "area" else feature
        operator_string = "most" if higher_operator else "least"
        header.title(f"What neighborhood has the :red[{operator_string} {feature_string}] in {district}")

        # prepare a dataframe for given question
        graph_df = ndf[ndf["district"] == district]
        # Exclude any records that do not have a numeric value (missing data)
        graph_df = graph_df[(graph_df[feature].notna()) & (graph_df[feature] != 0)]
        graph_df.reset_index(drop=True, inplace=True)
        # Get the correct answer for question
        target_feature_value = graph_df[feature].max() if higher_operator else graph_df[feature].min() # The target value of the given operator
        correct_record_idxs = graph_df.index[graph_df[feature] == target_feature_value].tolist()
        graph_df["is_correct"] = graph_df.index.isin(correct_record_idxs) # Add an answer key to the dataframe that will be true when correct

        # Create or get answers list, store it in session state to make sure answer reloading can not be abused when reloading current session
        if answers_key not in st.session_state or st.session_state[answers_key] is None:
            # Generate three random answers and the correct answer
            correct_residents_record = graph_df.loc[correct_record_idxs[0]].to_frame().T # Get the correct answer record
            answers = graph_df.loc[np.random.choice(graph_df.index[graph_df.index != correct_record_idxs[0]], 3, replace=False)] # Select 3 random records excluding the maximum residents record
            correct_residents_record["is_correct"] = correct_residents_record["is_correct"].astype(bool) # Set the is_correct col to bool explicitely to avoid future deprecation issues
            answers = pd.concat([answers, correct_residents_record]).sample(frac=1) # Add answer to other answers list, and shuffle the records
            st.session_state[answers_key] = answers
        else:
            answers = st.session_state[answers_key]
        
        with st.container():
            visual_col, answers_col = st.columns(2)
            with visual_col:
                fig = plt.figure(figsize=(5,3))
                fig.patch.set_facecolor('#0e1117') # Set the figure background to same as the page's background, lets hope it is not changed in the future
                # Create a bar chart
                plt.bar(range(len(graph_df)), graph_df[feature], color='red')

                # Set X-axis ticks to an empty list
                plt.xticks([])
                plt.tick_params(axis='y', colors='white')
                plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
                # Add labels and title
                plt.title(f'Number of {feature_string} per neighborhood', color="white")
                st.pyplot(fig)
            with answers_col:
                # Add some top padding
                st.markdown('')
                st.markdown('')
                st.markdown('')
                with st.container(border=True):
                    left_ans, right_ans = st.columns(2)
                    for i, (answer_idx, answer) in enumerate(answers.iterrows()):
                        answer_col = left_ans if i % 2 == 0 else right_ans # Spread answers evenly over left and right side by checking even/odd
                        answer_col.button(answer["neighborhood"], key=answer["neighborhood"], use_container_width=True, on_click=answer_classification_question, args=(answer,), disabled=state["completed"])
            
        if (state["completed"]):
            # Question has been completed so explain question
            if (st.button("Continue")):
                close_question()

            if (state["correct"]):
                st.header("CORRECT!", divider="rainbow") # Answer was correct
            else:
                st.header("wrong :(", divider="red") # Answer was wrong

            # Show a graph with the values, indicating the correct value
            fig = plt.figure(figsize=(8,5))
            fig.patch.set_facecolor('#0e1117') # Set the figure background to same as the page's background, lets hope it is not changed in the future
            # Create a bar chart
            plt.bar(range(len(graph_df)), graph_df[feature], color=['red' if is_correct else 'black' for is_correct in graph_df['is_correct']])  # Show the barchart again, but only make the highest (correct) value red

            plt.xticks(range(len(graph_df)), graph_df['neighborhood'], rotation=90, ha="center", color="white") # When rotated between 0-90 degrees the text shifts away from the xticks...
            plt.tick_params(axis='y', colors='white')
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
            
            plt.title(f'Number of {feature_string} per neighborhood ({operator_string} highlighted)', color="white")
            st.pyplot(fig)
    def numeric_open_question(district, feature, operation, error_margin_percentage = 10):
        """
        Parameters:
        - operation (str): one of the following operators:
            - 'lowest': find the lowest value.
            - 'median': find the median value.
            - 'highest': find the highest value.
        """
        feature_string = f"area in m\N{SUPERSCRIPT TWO}" if feature == "area" else feature
        header.title(f"Give the :red[{operation}] value for :red[{feature_string}] in {district}")
        header.markdown(f"*Within a {error_margin_percentage}% median margin*")

        # prepare a dataframe for given question
        graph_df = ndf[ndf["district"] == district]
        # Exclude any records that do not have a numeric value, but do include zero values
        graph_df = graph_df[graph_df[feature].notna()]
        graph_df.reset_index(drop=True, inplace=True)
        with header:
            with st.container():
                visual_col, answers_col = st.columns(2, gap="medium")
                with visual_col:
                    fig = plt.figure(figsize=(4,2))
                    fig.patch.set_facecolor('#0e1117') # Set the figure background to same as the page's background, lets hope it is not changed in the future

                    plt.boxplot(graph_df[feature], vert=False, widths=[0.60], medianprops={'color': "red"}, boxprops={'color': "red"}, whiskerprops={'color': "red"}, capprops={'color': "red"}, flierprops={'markeredgecolor': "red"})
                    plt.title(f"distribution of {feature_string} in neigborhoods", color="white")
                    plt.xticks([])
                    plt.yticks([])
                    st.pyplot(fig)
                with answers_col:
                    # Add some top padding
                    st.markdown('')
                    st.markdown('')
                    st.markdown('')
                    st.markdown('')
                    with st.container(border=True):
                        answer = st.number_input(f"{operation} value for {feature_string}", format="%i", step=1, value=None)
                        st.button("Submit", on_click=answer_open_question, args=(answer, graph_df[feature], operation, error_margin_percentage), disabled=state["completed"] or answer is None)
                
        if (state["completed"]):
            # Question has been completed so explain question
            if (st.button("Continue")):
                close_question()

            if (state["correct"]):
                st.header("CORRECT!", divider="rainbow") # Answer was correct
            else:
                st.header("wrong :(", divider="red") # Answer was wrong

            # Show a graph with the values, indicating the given from the expected value
            fig = plt.figure(figsize=(4,2))
            fig.patch.set_facecolor('#0e1117') # Set the figure background to same as the page's background, lets hope it is not changed in the future
            bp = plt.boxplot(graph_df[feature], vert=False, widths=[0.60], medianprops={'color': "black"})

            # Add indicator of acceptable range
            start_correct_range, end_correct_range = get_value_range(graph_df[feature], operation, error_margin_percentage)
            rectangle = Rectangle((start_correct_range, plt.ylim()[0]), end_correct_range - start_correct_range, plt.ylim()[1] - plt.ylim()[0], linewidth=2, edgecolor='red', facecolor='none')
            plt.gca().add_patch(rectangle)

            min_value = graph_df[feature].min()
            lower_percentile = bp['boxes'][0].get_xdata()[1]
            median = bp["medians"][0].get_xdata()[1]
            upper_percentile = bp['boxes'][0].get_xdata()[2]
            max_value = graph_df[feature].max()
            plt.yticks([])
            plt.tick_params(axis='x', colors='white')
            plt.xticks([min_value, lower_percentile, median, upper_percentile, max_value, start_correct_range, end_correct_range], color="white", rotation=90)
            plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
            
            plt.title(f"distribution of {feature_string} in neigborhoods", color="white")
            st.pyplot(fig)
    def multi_numeric_identification_question(district, featureX, featureY):
        featureX_string = f"area in m\N{SUPERSCRIPT TWO}" if featureX == "area" else featureX
        featureY_string = f"area in m\N{SUPERSCRIPT TWO}" if featureY == "area" else featureY
        header.title(f"What datapoint represents :red[{district}]")

        # prepare a dataframe for given question
        graph_df = ddf.copy()
        graph_df["char"] = [chr(ord('A') + i) for i in range(len(graph_df))]
        graph_df["is_correct"] = graph_df['district'] == district
        with header:
            with st.container():
                visual_col, answers_col, filler_col = st.columns([0.6, 0.3, 0.1])
                with visual_col:
                    fig = plt.figure(figsize=(5,3))
                    fig.patch.set_facecolor('#0e1117') # Set the figure background to same as the page's background, lets hope it is not changed in the future

                    plt.scatter(graph_df[featureX], graph_df[featureY], s=0)
                    # Add the visual char indicators
                    for i, district in graph_df.iterrows():
                        plt.text(district[featureX], district[featureY], district['char'], fontsize=12, ha='center', va='center')
                    plt.tick_params(axis='both', colors='white')
                    plt.xticks(rotation="90")
                    plt.xlabel(featureX_string, color="white")
                    plt.ylabel(featureY_string, color="white")
                    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
                    plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
                    plt.title(f'Districts of Eindhoven', color="white")
                    st.pyplot(fig)
                with answers_col:
                    # Add some top padding
                    st.markdown('')
                    st.markdown('')
                    st.markdown('')
                    with st.container(border=True):
                        for i, (answer_idx, answer) in enumerate(graph_df.iterrows()):
                            st.button(answer["char"], key=answer["char"], use_container_width=True, on_click=answer_classification_question, args=(answer,), disabled=state["completed"])
            
        if (state["completed"]):
            # Question has been completed so explain question
            if (st.button("Continue")):
                close_question()

            if (state["correct"]):
                st.header("CORRECT!", divider="rainbow") # Answer was correct
            else:
                st.header("wrong :(", divider="red") # Answer was wrong

            # Show a graph with the values, indicating the correct value
            fig = plt.figure(figsize=(8,5))
            fig.patch.set_facecolor('#0e1117') # Set the figure background to same as the page's background, lets hope it is not changed in the future

            plt.scatter(graph_df[featureX], graph_df[featureY], s=0)
            # Add the visual char indicators
            for i, district in graph_df.iterrows():
                plt.text(district[featureX], district[featureY], district['char'], fontsize=12, ha='center', va='center', color="red" if district["is_correct"] else "black")
            plt.tick_params(axis='both', colors='white')
            plt.xticks(rotation="90")
            plt.xlabel(featureX_string, color="white")
            plt.ylabel(featureY_string, color="white")
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
            plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
            plt.title(f'Districts of Eindhoven', color="white")
            st.pyplot(fig)
    def single_numeric_identification_question(district, feature):
        feature_string = f"area in m\N{SUPERSCRIPT TWO}" if feature == "area" else feature
        header.title(f"Which :red[{feature_string}] record represents :red[{district}]")

        # prepare a dataframe for given question
        graph_df = ddf.copy()
        graph_df["char"] = [chr(ord('A') + i) for i in range(len(graph_df))]
        graph_df["is_correct"] = graph_df['district'] == district
        with header:
            with st.container():
                visual_col, answers_col, filler_col = st.columns([0.6, 0.3, 0.1])
                with visual_col:
                    fig = plt.figure(figsize=(5,3))
                    fig.patch.set_facecolor('#0e1117') # Set the figure background to same as the page's background, lets hope it is not changed in the future

                    plt.bar(graph_df["char"], graph_df[feature], color='red')
                    plt.tick_params(axis='both', colors='white')
                    plt.ylabel(feature_string, color="white")
                    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
                    plt.title(f'Districts of Eindhoven', color="white")
                    st.pyplot(fig)
                with answers_col:
                    # Add some top padding
                    st.markdown('')
                    st.markdown('')
                    st.markdown('')
                    with st.container(border=True):
                        for i, (answer_idx, answer) in enumerate(graph_df.iterrows()):
                            st.button(answer["char"], key=answer["char"], use_container_width=True, on_click=answer_classification_question, args=(answer,), disabled=state["completed"])
            
        if (state["completed"]):
            # Question has been completed so explain question
            if (st.button("Continue")):
                close_question()

            if (state["correct"]):
                st.header("CORRECT!", divider="rainbow") # Answer was correct
            else:
                st.header("wrong :(", divider="red") # Answer was wrong

            # Show a graph with the values, indicating the correct value
            fig = plt.figure(figsize=(8,5))
            fig.patch.set_facecolor('#0e1117') # Set the figure background to same as the page's background, lets hope it is not changed in the future

            plt.bar(graph_df["char"], graph_df[feature], color=['red' if is_correct else 'black' for is_correct in graph_df['is_correct']])
            plt.tick_params(axis='both', colors='white')
            plt.ylabel(feature_string, color="white")
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
            plt.title(f'Districts of Eindhoven', color="white")
            st.pyplot(fig)

    state = st.session_state[state_key]

    # Question navigator
    if (state["difficulty"] == "easy"):
        if question_args_key not in st.session_state or st.session_state[question_args_key] is None:
            featureX = random.choice(numeric_features)
            featureY = random.choice(numeric_features)
            if (featureX == featureY):
                question_args = (state["district"], featureX) # Feature axises were the same, so store it once so that the correct function overload will be triggered 
            else:
                question_args = (state["district"], featureX, featureY)
            st.session_state[question_args_key] = question_args
        else:
            question_args = st.session_state[question_args_key]
        if (len(question_args) > 2):
            multi_numeric_identification_question(*question_args)
        else:
            single_numeric_identification_question(*question_args)
    elif (state["difficulty"] == "normal"):
        if question_args_key not in st.session_state or st.session_state[question_args_key] is None:
            question_args = (state["district"], random.choice(numeric_features), random.choice([True, False]))
            st.session_state[question_args_key] = question_args
        else:
            question_args = st.session_state[question_args_key]
        numeric_classification_question(*question_args)
    elif (state["difficulty"] == "hard"):
        if question_args_key not in st.session_state or st.session_state[question_args_key] is None:
            question_args = (state["district"], random.choice(numeric_features), random.choice(["lowest", "median", "highest"]))
            st.session_state[question_args_key] = question_args
        else:
            question_args = st.session_state[question_args_key]
        numeric_open_question(*question_args)
    else:
        # current state difficulty has no navigator so close question again
        close_question()
    
def close_question():
    st.session_state[answers_key] = None
    st.session_state[question_args_key] = None
    st.session_state[state_key] = None
    st.rerun() # Rerender display to show board again, as state has been cleared

# Renderer entrypoint
def main():
    # Create session state values
    # board information
    if board_key not in st.session_state:
        districts = ndf["district"].unique()
        difficulties = ["easy", "normal", "hard"]
        board_df = pd.DataFrame(index=difficulties, columns=districts)
        # Add the various metadata to all the possible options, this will make the cell values dictionaries
        # board_df.loc["easy", "Strijp"]["completed"] = completed value of the Strijp district on easy difficulty
        for district in districts:
            board_df.loc[:, district] = [{"district": district, "difficulty": difficulty, "prize": prize, "completed": False, "correct": False} for difficulty, prize in zip(difficulties, [100, 200, 400])]
        st.session_state[board_key] = board_df
    # points
    if points_key not in st.session_state:
        st.session_state[points_key] = 0
    # game state
    if state_key not in st.session_state:
        st.session_state[state_key] = None

    # Edit default styling
    # - center the headers of the columns
    st.markdown(
        """
        <style>
            [data-testid="column"] .stTextLabelWrapper { 
            justify-content: center !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    title_column, points_column = st.columns([0.8, 0.2], gap="small")
    points_column.header(f"prize: :red[${st.session_state[points_key]}]")
    
    if (st.session_state[state_key] == None):
        title_column.title("Eindhoven District Jeopardy")
        title_column.markdown("*Made by Thomas Van der Molen 🔧*")

        # Game is not within a current option, so show the board overview
        display_jeopardy_board()
    else:
        # a game state exists, so show the question
        display_question(title_column)
    
if __name__ == "__main__":
    main()