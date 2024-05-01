# pylint: disable=broad-except
"""
Neo4j Utilities
"""
from neo4j import GraphDatabase
import logging

def do_tx(tx, query, parameters):
    result = tx.run(query, parameters)
    values = []
    for record in result:
        values.append(record.values())
    return values

class Neo4jConnection:
    """
    Neo4j Connection class
    """

    def __init__(self):
        self.__uri = "neo4j://neo4j:7687"
        self.__user = "neo4j"
        self.__pwd = "your_password"
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(
                self.__uri, auth=(self.__user, self.__pwd)
            )
        except Exception as ex:
            logging.error("Failed to create the driver:", ex)

    def close(self):
        """
        Close connection
        """
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None):
        """
        Query the neo4j database
        """
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session()
            response = session.execute_read(do_tx, query, parameters)
        except Exception as ex:
            logging.error("Query failed:", ex)
        finally:
            if session is not None:
                session.close()
        return response
