import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('./data/mostrecent_data.csv')
df_cor = df.drop(columns=['Geoshape', 'GeoshapePerimeter', 'GeoshapeArea', 'GeoshapeCenter', 'NbId', 'DistrictId'])
st.write("# Correlations in Eindhoven by Stèphanie Smits")

st.table(df_cor)

fig, ax = plt.subplots()
sns.heatmap(df_cor.corr(), ax=ax)
st.write(fig)