import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import altair as alt
import plotly.express as px
from streamlit_folium import st_folium

data = pd.read_csv('fr-en-ecoles-effectifs-nb_classes.csv', delimiter = ';')

with st.sidebar:
    st.title('Visualisation of the number of students by Region / Department')
    
    year_list = list(data['rentree_scolaire'].unique())
    
    selected_year = st.selectbox('Select a year', year_list)
    df_selected_year = data[data['rentree_scolaire'] == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by='rentree_scolaire', ascending=False)

st.sidebar.subheader('Choice one or several regions')
plot_class = st.sidebar.multiselect('Select regions', options = data['region_academique'].unique())