import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to my Portfolio !")

st.sidebar.title('Social Networks :iphone:')
st.sidebar.write('Linkedin : (https://www.linkedin.com/in/hugo-heng-b176b0221/)')
st.sidebar.write('GitHub : (https://github.com/HugoHeng)')
st.sidebar.write('Twitter : ')

st.markdown(
    """
    Hello, my name is Hugo Heng, I'm 20 y.o and I live in France. Currently, I am a EFREI Paris student in Data & IA.
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)