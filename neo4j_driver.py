import os
from neo4j_driver import GraphDatabase

class Neo4jDriver:
    def __init__(self, uri, user, password):
        """Initialize the Neo4j driver with the given URI, user, and password."""
        self.driver = GraphDatabase.driver(uri, auth=(user,password))

    def close(self):
        """Close the Neo4j driver connection."""
        self.driver.close()

    def run_query(self, query, parameters=None):
        """
        Run a Cypher query against the Neo4j database.
        
        Args:
            query (str): The Cypher query to execute.
            parameters (dict, optional): Parameters for the query.
        
        Returns:
            list: Results of the query.
        """
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]    

    def get_driver(self):
        return self.driver