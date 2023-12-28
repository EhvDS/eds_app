import streamlit as st
import pandas as pd

# Loading the data
df_neighborhoods = pd.read_csv("./data/buurten_data_alex.csv", index_col=0)


st.title("15 Minutes City")

st.subheader("Find the closest path from A to B")