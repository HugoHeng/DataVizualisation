import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import altair as alt
import plotly.express as px
from streamlit_folium import st_folium

data = pd.read_csv('fr-en-ecoles-effectifs-nb_classes.csv', delimiter = ';')

# Prépa données #

data.rename(columns = {"nombre_eleves_cp_hors_ulis" : "Eleve de CP", 
    "nombre_eleves_ce1_hors_ulis" : "Eleve de CE1", 
    "nombre_eleves_ce2_hors_ulis" : "Eleve de CE2",
    "nombre_eleves_cm1_hors_ulis" : "Eleve de CM1",
    "nombre_eleves_cm2_hors_ulis" : "Eleve de CM2"}, inplace = True)

data_eleve = data.groupby('rentree_scolaire')[['Eleve de CP','Eleve de CE1','Eleve de CE2','Eleve de CM1','Eleve de CM2']].sum().reset_index()

data_eleve['rentree_scolaire'] = data_eleve['rentree_scolaire'].astype(str)

# Mise en page de l'interface

st.set_page_config(
    page_title="Number of classes & students in primary school at the start of the year",
    layout="wide",
    initial_sidebar_state="expanded")

#########################################################################################


# This sidebar offer us the choice of the date

with st.sidebar:
    st.title('Effective classes & students by year Dashboard')
    
    year_list = list(data['rentree_scolaire'].unique())
    
    selected_year = st.selectbox('Select a year', year_list)
    df_selected_year = data_eleve[data_eleve['rentree_scolaire'] == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by='rentree_scolaire', ascending=False)


# This sidebar offer us the choice of classes that we want see
st.sidebar.subheader('Choice of classes')
class_select = st.sidebar.multiselect('Select classes', ['Eleve de CP', 'Eleve de CE1', 'Eleve de CE2', 'Eleve de CM1', 'Eleve de CM2'], default = ['Eleve de CP'])

# Things that we put in my Dashboard #
st.markdown(f'### Linechart of Year {selected_year}')
st.line_chart(data_eleve, x = 'rentree_scolaire', y = class_select)

st.markdown('### Bar Chart for student')
st.bar_chart(data_eleve[['rentree_scolaire'] + class_select].set_index('rentree_scolaire'))


# Creation of columns

col = st.columns((2, 3, 1), gap = 'medium')