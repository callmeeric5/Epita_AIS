import streamlit as st

from neo4j_utils import Neo4jConnection

neo4j_connection = Neo4jConnection()

st.title("Movies")

title = st.text_input("Movie title")
button = st.button("Search for movies")
if "titles" not in st.session_state:
    st.session_state.titles = []

if "years" not in st.session_state:
    st.session_state.years = []

if "ratings" not in st.session_state:
    st.session_state.ratings = []

if button:
    if not title or (title and len(title) < 2):
        st.error("Input at least 2 characters of the movie")
    else:
        st.session_state.titles = neo4j_connection.query(
            "MATCH (m:Movie) WHERE m.title =~ $title RETURN m.title",
            {"title": ".*" + title + ".*"},
        )

option_title = st.selectbox(
    "Movie Title",
    [title[0] for title in st.session_state.titles],
    index=None,
    placeholder="Select a movie title",
)

if option_title:

    st.session_state.years = neo4j_connection.query(
        "MATCH (m:Movie) WHERE m.title = $title RETURN DISTINCT m.year",
        {"title": option_title},
    )


option_year = st.selectbox(
    "Movie Release Year",
    [year[0] for year in st.session_state.years],
    index=None,
    placeholder="Select a movie release year",
)

if option_year:
    st.session_state.ratings = neo4j_connection.query(
        "MATCH (m:Movie) WHERE m.title = $title AND m.year = $year RETURN DISTINCT m.rating",
        {"title": option_title, "year": option_year},
    )


option_rating = st.selectbox(
    "Movie Rating",
    [rating[0] for rating in st.session_state.ratings],
    index=None,
    placeholder="Select a movie rating",
)


if option_title and option_year and option_rating:
    movies = neo4j_connection.query(
        "MATCH (m:Movie) WHERE m.title = $title AND m.year = $year AND m.rating = $rating RETURN m.title, m.image",
        {"title": option_title, "year": option_year, "rating": option_rating},
    )
    if len(movies) == 0:
        st.write("No movies found")
    else:
        cols = st.columns(4)
        for idx, movie in enumerate(movies):
            cols[idx % 4].write(movie[0])
            cols[idx % 4].image(movie[1])
