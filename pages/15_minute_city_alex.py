import streamlit as st
import pandas as pd

# Loading the data
df_neighborhoods = pd.read_csv("./data/buurten_data_alex.csv", error_bad_lines=False)

print(df_neighborhoods.head())

st.title("15 Minutes City")

st.subheader("Find the closest path from A to B")


st.dataframe(df_neighborhoods)