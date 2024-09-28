import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import altair as alt
import plotly.express as px
from streamlit_folium import st_folium

data = pd.read_csv('fr-en-ecoles-effectifs-nb_classes.csv', delimiter = ';')

# ---------------------- #

st.set_page_config(
    page_title="Main Page",
    page_icon = "bar_chart"
)

st.sidebar.markdown("# Welcome to my Streamlit Dashboard !")

st.write("# Dashboard of the effective of classes & students in a class (2019 - 2023)")

st.dataframe(data)

# st.markdown()