import streamlit as st

from neo4j_utils import Neo4jConnection

neo4j_connection = Neo4jConnection()


st.title("Movie Actors")

name = st.text_input("Actor name")
button = st.button("Search for actors")

if "actors" not in st.session_state:
    st.session_state.actors = []

if button:
    if not name or (name and len(name) < 2):
        st.error("Input at least 2 characters of the name")
    else:
        st.session_state.actors = neo4j_connection.query(
            "MATCH (n:Actor) WHERE n.name =~ $name RETURN n.name",
            {"name": ".*" + name + ".*"},
        )

option = st.selectbox(
    "Actor Name",
    [actor[0] for actor in st.session_state.actors],
    index=None,
    placeholder="Select an Actor",
)

if option:
    movies = neo4j_connection.query(
        "MATCH (n:Actor)-[:ACTED_IN]->(m:Movie) WHERE n.name = $name RETURN m.title, m.image, m.year, m.rating",
        {"name": option},
    )
    if len(movies) == 0:
        st.write("No movies found")
    else:
        cols = st.columns(4)
        for idx, movie in enumerate(movies):
            cols[idx % 4].write(movie[0])
            cols[idx % 4].image(movie[1])
