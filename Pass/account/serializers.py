from rest_framework import serializers

class UserSignupSerializer(serializers.Serializer):
    firstName = serializers.CharField(max_length=255)
    lastName = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=20)
    role_id = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, min_length=6)

class KYCSerializer(serializers.Serializer):
    documentType = serializers.IntegerField(min_value =1, max_value=3, required=True)
    documentNumber = serializers.CharField(max_length=255, required=True)
    documentURL = serializers.CharField(max_length=None, required=True)
    user_id = serializers.CharField(max_length=None, required=True)

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255)
    # role_id = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, min_length=6)