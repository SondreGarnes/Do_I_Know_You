from typing import Any
from neo4j import GraphDatabase
from neo4j_connection import Neo4jConnection
class UserModel:
    def __init__(self):
        self._connection = Neo4jConnection()

    def close(self):
        self._connection.close()

    def create_user(self, name, email):
        with self._connection._driver.session() as session:
            session.write_transaction(self._create_user, name, email)

    @staticmethod
    def _create_user(tx, name, email):
        tx.run("CREATE (a:User {name: $name, email: $email})", name=name, email=email)