from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .neo4j_connection import Neo4jConnection
# Create your views here.


class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            email = serializer.validated_data.get('email')
            neo4j_connection = Neo4jConnection()
            create_user_query = "CREATE (u:User {name: $name, email: $email}) RETURN u"
            neo4j_connection.run_query(create_user_query, {"name": name, "email": email})
            neo4j_connection.close()
            return Response({"message": "User created."}, status=201)
        return Response(serializer.errors, status=400)