"""
Streamlit web app
"""

import streamlit as st
from st_pages import Page, add_page_title, show_pages

show_pages(
    [
        Page("streamlit_app.py", "Home", "🏠"),
        Page("actors.py", "Actorz", "🧑"),
        Page("movies.py", "Moviez", "🎥"),
    ]
)

st.set_page_config(page_title="Home", page_icon="🏠")
st.title("Movie Database - With Neo4j")
