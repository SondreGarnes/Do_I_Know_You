from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
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
            create_user_query = "CREATE (u:User {first_name: $first_name, last_name: $last_name, email: $email, password: $password}) RETURN u"
            neo4j_connection.run_query(create_user_query, {"first_name":first_name,"last_name":last_name
                                                           , "email": email, "password":hashed_password}) 
            neo4j_connection.close()
            return Response({"message": "User created."}, status=201)
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
        get_users_query = "MATCH (u:User) RETURN u.first_name as first_name, u.last_name as last_name, u.email as email"
        users = neo4j_connection.run_query(get_users_query)
        users_list = [{"first_name": record["first_name"],"last_name":record["last_name"], "email": record["email"]} for record in users]
        neo4j_connection.close()
        return Response(users_list, status=200)
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            neo4j_connection = Neo4jConnection()
            get_user_query = "MATCH (u:User {email: $email}) RETURN u.password as password"
            user = neo4j_connection.run_query(get_user_query, {"email": email})
            if user:
                hashed_password = user[0]["password"]
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    request.session['email'] = email
                    return Response({"message": "Login successful."}, status=200)
            neo4j_connection.close()
        return Response({"message": "Invalid credentials."}, status=400)
class LogoutView(APIView):
    def get(self, request):
        request.session.flush()
        return Response({"message": "User logged out."}, status=200)
class CheckLoginStatus(APIView):
    def get(self, request):
        if request.session.get('email'):
            return Response({"message": "User is logged in."}, status=200)
        return Response({"message": "User is not logged in."}, status=200)
