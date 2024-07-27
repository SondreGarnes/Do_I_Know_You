from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer, RelationshipSerializer
from .neo4j_connection import Neo4jConnection
import bcrypt
# Create your views here.


class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            neo4j_connection = Neo4jConnection()
            create_user_query = """
                CREATE (u:User {first_name: $first_name, last_name: $last_name, email: $email, password: $password}) 
                RETURN id(u) as id, u.first_name as first_name, u.last_name as last_name
            """
            result = neo4j_connection.run_query(create_user_query, {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": hashed_password
            })
            neo4j_connection.close()
            if result:
                user_id = result[0]["id"]
                return Response({
                    "message": "User created.",
                    "id": user_id,
                    "first_name": first_name,
                    "last_name": last_name
                }, status=201)
        return Response(serializer.errors, status=400)
    
class DeleteUsers(APIView):
    def post(self, request):
        neo4j_connection = Neo4jConnection()
        delete_users_query = "MATCH (u:User) DETACH DELETE u"
        neo4j_connection.run_query(delete_users_query)
        neo4j_connection.close()
        return Response({"message": "All users deleted."}, status=200)
    
class GetUsers(APIView):
    def get(self, request):
        neo4j_connection = Neo4jConnection()
        get_users_query = "MATCH (u:User) RETURN elementId(u) as id, u.first_name as first_name, u.last_name as last_name, u.email as email"
        users = neo4j_connection.run_query(get_users_query)
        users_list = [{"id": record["id"], "first_name": record["first_name"], "last_name": record["last_name"], "email": record["email"]} for record in users]
        neo4j_connection.close()
        return Response(users_list, status=200)
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            neo4j_connection = Neo4jConnection()
            get_user_query = """
                MATCH (u:User {email: $email}) 
                RETURN u.password as password, u.first_name as first_name, u.last_name as last_name, elementId(u) as id
            """
            user = neo4j_connection.run_query(get_user_query, {"email": email})
            if user:
                hashed_password = user[0]["password"]
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    request.session['email'] = email
                    user_id = user[0]["id"]
                    first_name = user[0]["first_name"]
                    last_name = user[0]["last_name"]
                    return Response({
                        "message": "Login successful.",
                        "first_name": first_name,
                        "last_name": last_name,
                        "id":user_id
                    }, status=200)
            neo4j_connection.close()
        return Response({"message": "Invalid credentials."}, status=400)
class LogoutView(APIView):
    def get(self, request):
        request.session.flush()
        return Response({"message": "User logged out."}, status=200)
class CheckLoginStatus(APIView):
    def get(self, request):
        email = request.session.get('email')
        if email:
            neo4j_connection = Neo4jConnection()
            get_user_query = """
                MATCH (u:User {email: $email}) 
                RETURN u.id as id, u.first_name as first_name, u.last_name as last_name
            """
            user = neo4j_connection.run_query(get_user_query, {"email": email})
            if user:
                user_id = user[0]["id"]
                first_name = user[0]["first_name"]
                last_name = user[0]["last_name"]
                return Response({
                    "message": "User is logged in.",
                    "id": user_id,
                    "first_name": first_name,
                    "last_name": last_name
                }, status=200)
            neo4j_connection.close()
        return Response({"message": "User is not logged in."}, status=200)
class AddRelationship(APIView):
    def post(self, request):
        serializer = RelationshipSerializer(data=request.data)
        if serializer.is_valid():
            user1_id = serializer.validated_data.get('user1_id')
            user2_id = serializer.validated_data.get('user2_id')
            
            neo4j_connection = Neo4jConnection()
            
            # Check if the relationship already exists
            check_relationship_query = """
                MATCH (u1:User)-[r:FRIEND]->(u2:User)
                WHERE elementId(u1) = $user1_id AND elementId(u2) = $user2_id
                RETURN type(r) as relationship_type
            """
            try:
                existing_relationship = neo4j_connection.run_query(check_relationship_query, {
                    "user1_id": user1_id,
                    "user2_id": user2_id
                })
                
                if existing_relationship:
                    neo4j_connection.close()
                    return Response({
                        "message": "Users are already friends.",
                        "relationship_type": existing_relationship[0]["relationship_type"]
                    }, status=200)
                
                # Add the new relationship if it doesn't exist
                add_relationship_query = """
                    MATCH (u1:User), (u2:User)
                    WHERE elementId(u1) = $user1_id AND elementId(u2) = $user2_id
                    CREATE (u1)-[r:FRIEND]->(u2)
                    RETURN type(r) as relationship_type
                """
                result = neo4j_connection.run_query(add_relationship_query, {
                    "user1_id": user1_id,
                    "user2_id": user2_id
                })
                neo4j_connection.close()
                
                if result:
                    return Response({
                        "message": "Relationship created.",
                        "relationship_type": result[0]["relationship_type"]
                    }, status=201)
            except Exception as e:
                # Log the exception
                print(f"Error creating relationship: {e}")
                return Response({"error": "Internal Server Error"}, status=500)
        else:
            # Log serializer errors
            print(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=400)
class GetRelationships(APIView):
    def get(self, request):
        neo4j_connection = Neo4jConnection()
        get_relationships_query = """
            MATCH (u1:User)-[r:FRIEND]->(u2:User)
            RETURN elementId(u1) as user1_id, elementId(u2) as user2_id, type(r) as relationship_type
        """
        try:
            result = neo4j_connection.run_query(get_relationships_query)
            neo4j_connection.close()
            
            # Log the result to inspect the data
            print("Relationships fetched:", result)
            
            return Response(result, status=200)
        except Exception as e:
            # Log the exception
            print(f"Error fetching relationships: {e}")
            return Response({"error": "Internal Server Error"}, status=500)

class DeleteRelationships(APIView):
    def post(self, request):
        neo4j_connection = Neo4jConnection()
        delete_relationships_query = "MATCH ()-[r:FRIEND]->() DELETE r"
        neo4j_connection.run_query(delete_relationships_query)
        neo4j_connection.close()
        return Response({"message": "All relationships deleted."}, status=200)