from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.conf import settings
import boto3
from .import models
from .serializers import UserSignupSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserSignupView(CreateAPIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        print("ENTER FUNCION")
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        firstName = serializer.validated_data.get('firstName')
        lastName = serializer.validated_data.get('lastName')
        phone_number = "+91" + serializer.validated_data.get('phone_number')
        user_group = serializer.validated_data.get('user_group')
        password = serializer.validated_data.get('password')

        # Create a user object in your PostgreSQL database
        user = models.User.objects.create(first_name=firstName, last_name=lastName, phone_number=phone_number, user_group=user_group)
        print(">>>>>>>>>>>>>>>>>>>>")
        # Create user in AWS Cognito
        cognito_client = boto3.client('cognito-idp', region_name=settings.AWS_COGNITO_REGION)
        response = cognito_client.sign_up(
            ClientId=settings.AWS_COGNITO_APP_CLIENT_ID,
            Username=phone_number,
            Password=password,
            UserAttributes=[
                {'Name': 'phone_number', 'Value': phone_number},
                {'Name': 'family_name', 'Value': lastName},
                {'Name': 'given_name', 'Value': firstName},
                {'Name': 'custom:role_id', 'Value': user_group}

            ]
        )
        # groupName=""
        # if user_group == "1":
        #     groupName="cust"
        # else:
        #     groupName="agentSSS"
        # groupResponse = cognito_client.create_group(UserPoolId=settings.USER_POOL_ID,  GroupName=groupName)
        # response = cognito_client.admin_add_user_to_group(
        #     UserPoolId=settings.USER_POOL_ID,
        #     Username=phone_number,
        #     GroupName=groupName
        # )
        print("<<<<<<<<<<<<<<<<<<<<<<<<<", response)
        # Save Cognito user ID to the user model
        user.user_id = response['UserSub']
        user.save()

        # Trigger OTP generation and sending process using AWS Cognito
        # Add code to send OTP to the user's phone number

        return Response({'message': 'User signed up successfully.'})
