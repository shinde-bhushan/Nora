from rest_framework import serializers

class UserSignupSerializer(serializers.Serializer):
    firstName = serializers.CharField(max_length=255)
    lastName = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=20)
    user_group = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, min_length=6)

