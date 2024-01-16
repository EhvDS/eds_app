import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import random

df = pd.read_csv('./data/mostrecent_data.csv')
if 'question_scores' not in st.session_state:
    st.session_state['question_scores'] = list()
    for i in range(0, 7):
        st.session_state['question_scores'].append(-1)

if 'question_page' not in st.session_state:
    st.session_state['question_page'] = 0

def change_question(increment):
    st.session_state['question_page'] += increment

def check_correct(choice):
    if str(choice) == str(question_choices[st.session_state['question_page']][2]):
        st.session_state['question_scores'][st.session_state['question_page']] = 1
    else:
        st.session_state['question_scores'][st.session_state['question_page']] = 0

# All predifined Questions
questions = ['What district is the most a?',
                'What district is the most b?',
                'What district is the most c?',
                'What district is the most d?',
                'What district is the most e?',
                'What district is the most f?',
                'What district is the most g?']

# All predefined answers
question_choices = [[1, 2, 3, 4],
                    ['a', 'b', 'c', 'd'],
                    [5, 6, 7, 8],
                    ['e', 'f', 'g', 'h'],
                    [325, 'pi', 3000, 'sqrt(2)'],
                    ['Brazil', 'Omicron', 'Watermelon', 'Medical Engineering'],
                    ['Cat', 'Dog', 'Lizard', 'Hamster']]

question_media = []

st.title('Quiz Time!')
st.header(questions[st.session_state['question_page']])

## TODO Question Graph/table/etc goes here
st.map(data=df, latitude=5.496376105740801, longitude=51.496778766905756)

## Answer layout
container = st.container(border=True)
col1, col2 = container.columns(2)

## Answer position randomizer
choices = random.sample(question_choices[st.session_state['question_page']], 4)

# Answers
with col1:
    st.button(label = str(choices[0]), on_click=check_correct, args=[str(choices[0])])
    st.button(label = str(choices[1]), on_click=check_correct, args=[str(choices[1])])
with col2:
    st.button(label = str(choices[2]), on_click=check_correct, args=[str(choices[2])])
    st.button(label = str(choices[3]), on_click=check_correct, args=[str(choices[3])])

# Question Navigation layout
col3, col4 = st.columns(2)

# Question navigation buttons
with col3:
    if st.session_state['question_page'] > 0:
        st.button('Previous Question', on_click=change_question, args=[-1], disabled=st.session_state['question_page'] <= 0)
with col4:
    if st.session_state['question_page'] < 6:
        st.button('Next Question', type='primary', on_click=change_question, args=[1], disabled=st.session_state['question_scores'][st.session_state['question_page']] == -1)

# TODO Remove DEBUG writes below 
st.write(st.session_state['question_page'])
st.write(st.session_state['question_scores'])
