from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

class RelationshipSerializer(serializers.Serializer):
    user1_id = serializers.CharField()
    user2_id = serializers.CharField()