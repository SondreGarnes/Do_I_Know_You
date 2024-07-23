import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

class Neo4jConnection:
    def __init__(self):
        uri=os.getenv("NEO4J_URI")
        user=os.getenv("NEO4J_USER")
        password=os.getenv("NEO4J_PASSWORD")

        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()
    
    def run_query(self, query, parameters=None):
        with self._driver.session() as session:
            return session.run(query, parameters)
        