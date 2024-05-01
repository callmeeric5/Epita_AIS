# Neo4j Movies Repository

## Docker Compose

This project uses docker compose. Docker Compose is a tool for defining and running multi-container applications.

To launch this web application, you can run the following command, from the root folder of the project.

```
git clone git@github.com:Eliie58/neo4j_movies_repository.git
cd neo4j_movies_repository
docker compose up -d --build
```

### Database

The neo4j database is accesible from [http://localhost:7474/browser/](http://localhost:7474/browser/)

### Web Application

The web application, deployed using [Streamlit](https://streamlit.io/) is accesible from [http://localhost:8080](http://localhost:8080)

## Data Loading

Data used is available under the [data](./data/) folder.

To load the data into the database, you can use the following commands:

```
CREATE INDEX movie_title FOR (n:Movie) ON (n.title);
CREATE INDEX genre_name FOR (n:Genre) ON (n.name);
CREATE INDEX actor_name FOR (n:Actor) ON (n.name);

:auto LOAD CSV WITH HEADERS FROM 'file:///movies.csv' AS row

CALL {
    with row
    MERGE (a:Movie {title: row.title, year: toInteger(row.year), image: row.image, rating: toFloat(row.rating)})

    FOREACH (genre in split(row.genre, "|") |
        MERGE (b:Genre {name: genre})
        MERGE (b)-[:GENRE_OF]->(a)
    )

    FOREACH (actor in split(row.actors, "|") |
        MERGE (c:Actor {name: actor})
        MERGE (c)-[:ACTED_IN]->(a)
    )
} IN TRANSACTIONS OF 100 ROWS;

LOAD CSV WITH HEADERS FROM 'file:///actors.csv' AS row
MERGE (a:Actor {name: row.name})
SET a.image= row.image_path;
```
