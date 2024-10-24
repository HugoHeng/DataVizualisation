import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import plotly.express as px
from streamlit_folium import st_folium
import folium
from folium import Choropleth
import json

geojson = 'departements.geojson'

data = pd.read_csv('fr-en-ecoles-effectifs-nb_classes.csv', delimiter = ';')

# Prépa données #

with open(geojson, 'r', encoding='utf-8') as file:
    geojson_dep = json.load(file)

data.rename(columns = {
    "nombre_eleves_preelementaire_hors_ulis" : "Eleve Maternelle Total",
    "nombre_eleves_ulis" : "Eleve en Handicap",
    "nombre_eleves_elementaire_hors_ulis" : "Eleve Élémentaire Total", 
    "nombre_eleves_cp_hors_ulis" : "Eleve de CP", 
    "nombre_eleves_ce1_hors_ulis" : "Eleve de CE1", 
    "nombre_eleves_ce2_hors_ulis" : "Eleve de CE2",
    "nombre_eleves_cm1_hors_ulis" : "Eleve de CM1",
    "nombre_eleves_cm2_hors_ulis" : "Eleve de CM2"}, inplace = True)

data_eleve = data.groupby('rentree_scolaire')[['Eleve Maternelle Total','Eleve de CP','Eleve de CE1','Eleve de CE2','Eleve de CM1','Eleve de CM2']].sum().reset_index()
data_departement = data.groupby(['departement', 'rentree_scolaire'])[['nombre_total_eleves', 'Eleve Maternelle Total']].sum().reset_index()
data_region = data.groupby(['region_academique', 'rentree_scolaire'])[['nombre_total_eleves', 'Eleve Élémentaire Total', 'Eleve Maternelle Total', 'Eleve en Handicap', 'Eleve de CP','Eleve de CE1','Eleve de CE2','Eleve de CM1','Eleve de CM2']].sum().reset_index()
data_academie = data.groupby(['academie', 'rentree_scolaire'])[['nombre_total_eleves', 'Eleve Élémentaire Total', 'Eleve Maternelle Total', 'Eleve en Handicap']].sum().reset_index()
data['code_postal'] = data['code_postal'].astype(str).str.zfill(5)
data['code_departement'] = data['code_postal'].str[:2]
departement_code_unique = data[['departement', 'code_departement']].drop_duplicates().reset_index()
data_departement = data_departement.merge(departement_code_unique, on='departement', how='left')

data_eleve['rentree_scolaire'] = data_eleve['rentree_scolaire'].astype(str)
data_departement['rentree_scolaire'] = data_departement['rentree_scolaire'].astype(str)
data_region['rentree_scolaire'] = data_region['rentree_scolaire'].astype(str)
data_academie['rentree_scolaire'] = data_academie['rentree_scolaire'].astype(str)

merged_data = pd.merge(data_departement, data_eleve, on='rentree_scolaire', how='outer')

# Mise en page de l'interface

st.set_page_config(
    page_title="Number of classes & students in primary school at the start of the year",
    layout="wide",
    initial_sidebar_state="expanded")

#########################################################################################

# This sidebar offer us the choice of the date

with st.sidebar:
    st.title('Effective classes & students by year Dashboard')
    
    year_list = sorted(list(merged_data['rentree_scolaire'].unique()), reverse=True)
    selected_year = st.selectbox('Select a year', year_list)
    
    df_selected_year = merged_data[merged_data['rentree_scolaire'] == selected_year]
    df_selected_year = df_selected_year.sort_values(by=['rentree_scolaire', 'nombre_total_eleves'], ascending=False)

    st.sidebar.subheader('Choice of classes')
    class_select = st.sidebar.multiselect('Select classes', ['Eleve Maternelle Total','Eleve de CP', 'Eleve de CE1', 'Eleve de CE2', 'Eleve de CM1', 'Eleve de CM2'], default = ['Eleve de CP'])

st.header("📊 **_Dashboard of the effective of students in a class (2019 - 2023)_**", divider = True)
st.dataframe(data)
# Choropleth for France

for feature in geojson_dep['features']:
    feature['properties']['code'] = feature['properties']['code'].upper() 

m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

df_selected_year1 = data_departement[data_departement['rentree_scolaire'] == selected_year]
df_selected_year1['departement'] = data_departement['departement'].astype(str)
df_selected_year1['departement'] = df_selected_year1['departement'].str.upper().str.replace(' ', '-')
df_selected_year1['code_departement'] = data_departement['code_departement'].astype(str).str[:2]

Choropleth(
    geo_data=geojson_dep, 
    name="Choropleth",
    data=df_selected_year1,
    columns=['code_departement', 'nombre_total_eleves'], 
    key_on="feature.properties.code",
    fill_color="YlOrRd", 
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Number of students by departement",
).add_to(m)

folium.LayerControl().add_to(m)

# Creation of columns

df_selected_region_year = data_region[data_region['rentree_scolaire'] == selected_year]
df_selected_academie = data_academie[data_academie['rentree_scolaire'] == selected_year]
top_academie = df_selected_academie.nlargest(15, 'nombre_total_eleves')

col1, col2 = st.columns([2, 3])

with col1:
    st.dataframe(df_selected_year,
             column_order=("departement", "nombre_total_eleves", "Eleve Maternelle Total_x"),
             hide_index=True,
             column_config={
                "departement": st.column_config.TextColumn("Departement"),
                "nombre_total_eleves": st.column_config.ProgressColumn("Total Number of Students",
                    format="%d",
                    min_value=0,
                    max_value=max(df_selected_year["nombre_total_eleves"])),
                "Eleve Maternelle Total_x": st.column_config.ProgressColumn("Total Number of Nursery Students",
                    format="%d",
                    min_value=0,
                    max_value=max(df_selected_year["Eleve Maternelle Total_x"])),
                }
            )

    fig = px.pie(top_academie, values='nombre_total_eleves', names='academie',
                title=f"Repartition of total student by the 15 best academia in {selected_year}")
    st.plotly_chart(fig)
                
total_eleves = df_selected_region_year['nombre_total_eleves'].sum()
eleves_handicap = df_selected_region_year['Eleve en Handicap'].sum()
eleves_maternelle = df_selected_region_year['Eleve Maternelle Total'].sum()
proportion_maternelle = (eleves_maternelle / total_eleves) * 100
max_academie = data_academie[data_academie['rentree_scolaire'] == selected_year].nlargest(1, 'nombre_total_eleves')
academie_name = max_academie['academie'].values[0]
number_eleve = max_academie['nombre_total_eleves'].values[0]

with col2:
    subcol1, subcol2 = st.columns(2)

    st.markdown('### Department Map - Heatmap')
    st_folium(m, width=700, height=500)

    subcol1.metric(label="Total number of students", value = total_eleves)
    subcol1.metric(label="Total number of students with disabilities", value = eleves_handicap)

    subcol2.metric(label='Proportion of nursery students out of the total number of students', value = f"{proportion_maternelle:.2f}%")
    subcol2.metric(label="Academy with the most students", value=number_eleve, delta=f"{academie_name}")
    
st.markdown('---')

df_region_melt = df_selected_region_year.melt(id_vars='region_academique', 
                                    value_vars=class_select, 
                                    var_name='Classe', 
                                    value_name="Number of student")

fig = px.bar(df_region_melt, 
             x='region_academique', 
             y="Number of student", 
             color='Classe', 
             barmode='group',
             title=f"Répartition of student by region in year {selected_year}",
             labels={'region_academique': 'Région académique', "Number of student": "Number of student"})

st.plotly_chart(fig)

df_region_melt = df_selected_region_year.melt(id_vars='region_academique', 
                                            value_vars=['nombre_total_eleves', 'Eleve Élémentaire Total', 'Eleve Maternelle Total', 'Eleve en Handicap'], 
                                            var_name='Catégorie', 
                                            value_name='Nombre')

fig = px.bar(df_region_melt, x='region_academique', y='Nombre', color='Catégorie', barmode='group',
                title=f"Repartition of students for the year {selected_year}",
                labels={'region_academique': 'Academic Region', 'Nombre': "Number of student"})

st.plotly_chart(fig)

