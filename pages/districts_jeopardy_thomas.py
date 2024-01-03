import pandas as pd
import streamlit as st

# Keys used to store states persistently
board_key = "thomas_jeopardy_board"
points_key = "thomas_jeopardy_points"
state_key = "thomas_jeopardy_state"

def create_board_df():
    districts = ["Strijp", "Woensel-Noord", "Woensel-Zuid", "Centrum", "Tongelre", "Gestel", "Stratum"]
    difficulties = ["easy", "normal", "hard"]
    board_df = pd.DataFrame(index=difficulties, columns=districts)
    # Add the various metadata to all the possible options, this will make the cell values dictionaries
    # board_df.loc["easy", "Strijp"]["completed"] = completed value of the Strijp district on easy difficulty
    for district in districts:
        board_df.loc[:, district] = [{"difficulty": difficulty, "prize": prize, "completed": False} for difficulty, prize in zip(difficulties, [100, 200, 400])]

    return board_df

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
                        if st.button(f"{option['difficulty']} (${option['prize']})", key=f"{district}-{option['difficulty']}", use_container_width=True, disabled=option["completed"]):
                            # Button on click logic
                            # Store the selected option in the current state
                            st.session_state[state_key] = option
                            st.rerun() # Disgustingly re-render, to make sure the renderer is properly representing the changes made

# Renderer entrypoint
def main():
    # Set the page layout to wide view, so that horizontal space is available on large screens
    st.set_page_config(layout="wide") 

    # Create session state values
    # board information
    if board_key not in st.session_state:
        st.session_state[board_key] = create_board_df()
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
    title_column.title("Eindhoven Jeopardy Game")
    
    points_column.header(f"prize: :red[${st.session_state[points_key]}]")
    
    if (st.session_state[state_key] == None):
        # Game is not within a current option, so show the board overview
        display_jeopardy_board()
    else:
        board_option = st.session_state[state_key]
        # Game has a selected option
        if st.button("complete! (placeholder)"):
            # Complete game, give points of option and reset the state
            st.session_state[points_key] = st.session_state[points_key] + board_option["prize"]
            board_option["completed"] = True
            st.session_state[state_key] = None

            st.rerun()
    


if __name__ == "__main__":
    main()