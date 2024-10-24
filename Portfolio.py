import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium
import plotly.express as px


skills = {
    'Skills': ['Python', 'MySQL', 'Scikit-Learn', 'Machine Learning', 'Matplotlib', 'Pandas'],
    'Percentage': [20, 10, 15, 15, 30, 30]
}

project_time = {
    'Project': ['Project DVF', 'Project Brevet', 'Project Data Vizualisation'],
    'Start': ['2023-06-20', '2023-07-01', '2023-09-09'],
    'Finish': ['2023-06-30', '2023-07-26', '2023-10-22'],
}

#################

st.set_page_config(
    page_title="Portfolio",
    layout="wide"
)

st.sidebar.title('Social Networks :iphone:')
st.sidebar.write('Linkedin : [My Linkedin](https://www.linkedin.com/in/hugo-heng-b176b0221/)')
st.sidebar.write('GitHub : [My GitHub](https://github.com/HugoHeng)')
st.sidebar.write('Twitter : [My Twitter](https://x.com/elonmusk)')
st.sidebar.write('Email : hugo.heng@efrei.net')

st.title("_Hugo HENG - Portfolio_ 📊")
st.header("Presentation 🧑‍💻", divider = True)
st.markdown("""
    Hello ! My name is Hugo HENG, I'm 20 years old and I live in France. Currently, I study at EFREI Paris
    in the Data & IA major. For 2 years, I have been interested in Data Science because I love exploring new datasets, 
    testing algorithms and continually learning.  
""")

with open("CV Hugo HENG.pdf", "rb") as file:
    resume = file.read()

st.download_button(
    label = '📥 Download Resume',
    data = resume,
    file_name = "CV Hugo HENG.pdf",
    mime="application/pdf"
)

st.header("Skills 🛠️", divider = True)
col1, col2 = st.columns(2)
with col1:
    data = pd.DataFrame(skills)
    fig = px.pie(data, values='Percentage', names='Skills')
    st.plotly_chart(fig)

with col2:
    skills = ['Communication', 'Collaboration', 'Gestion of time', 'Adaptibility', 'Problem Resolution', 'Critical Thinking']
    values = [9, 8, 6, 7, 6.5, 7]

    for skill, value in zip(skills, values):
        st.write(skill)
        st.progress(value / 10)

st.header("Projects 🚀", divider = True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### Project DVF 🏢")
    st.image('dvf.jpg')
    st.markdown('This project aimed to predict the price of real estate')
    st.markdown('To see more : [Project DVF](https://github.com/HugoHeng/prj_data_science/settings/access?guidance_task=)')
with col2:
    st.markdown("### Project about Brevet 📜")
    st.image('brevet-innovation.jpg')
    st.markdown('This project aimed to classify a Brevet depending of the type')
    st.markdown('To see more  : [Project EXPLAIN]()')
with col3:
    st.markdown("### Project of Vizualisation 🏫")
    st.image('ecole-lamartine.jpg')
    st.markdown('This project aimed to visualize Data from student')
    st.markdown('To see more  : [Project DataViz](http://localhost:8501/Dashboard)')

st.header("Timeline of my project", divider = True)
fig = px.timeline(project_time, x_start='Start', x_end='Finish', y = 'Project', title='Projets & Duration')
st.plotly_chart(fig)