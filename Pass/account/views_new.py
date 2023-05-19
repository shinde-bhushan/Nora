from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.conf import settings
import boto3
from .import models
from .serializers import UserSignupSerializer, KYCSerializer, UserLoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


# API class for User Registeration in AWS Cognito
class UserSignupView(CreateAPIView):
    permission_classes = [AllowAny,]

    # Below POST method is used for creation of User in Cognito with required fields only and link the user with the respective Group.

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        firstName = serializer.validated_data.get('firstName')
        lastName = serializer.validated_data.get('lastName')
        phone_number = "+91" + serializer.validated_data.get('phone_number')
        role_id = serializer.validated_data.get('role_id')
        password = serializer.validated_data.get('password')

        groupName=""
        if role_id == "4":
            groupName="customers"
        if role_id == "3":
            groupName="agents"
        if role_id == "2":
            groupName="merchants"
        if role_id == "1":
            groupName="super-admin"

        # Create user in AWS Cognito
        try:
            cognito_client = boto3.client('cognito-idp', region_name=settings.AWS_COGNITO_REGION)
            response = cognito_client.sign_up(
                ClientId=settings.AWS_COGNITO_APP_CLIENT_ID,
                Username=phone_number,
                Password=password,
                UserAttributes=[
                    {'Name': 'phone_number', 'Value': phone_number},
                    {'Name': 'family_name', 'Value': lastName},
                    {'Name': 'given_name', 'Value': firstName},
                    {'Name': 'custom:role_id', 'Value': role_id}
                ]
            )
            
            # If user created successfully then it will link to the Group
            if (response['ResponseMetadata']['HTTPStatusCode']) == 200:
                groupResponse = cognito_client.admin_add_user_to_group(
                    UserPoolId=settings.USER_POOL_ID,
                    Username=phone_number,
                    GroupName=groupName
                )              
       
        except cognito_client.exceptions.UsernameExistsException as e:
            result = f"An account with the given Phone number already exists."
        except Exception as e:
            response = cognito_client.admin_delete_user(
                UserPoolId=settings.USER_POOL_ID,
                Username=phone_number
            )
            result = f"User Not Registered Successfully {e}."
        else:
            # Create a user object in your PostgreSQL database
            user = models.User.objects.create(first_name=firstName, last_name=lastName, phone_number=phone_number, role_id=role_id)
            # Save Cognito user ID to the user model when there's no error.
            user.user_id = response['UserSub']
            user.save()
            result = f"User created successfully."
        # Trigger OTP generation and sending process using AWS Cognito
        # Add code to send OTP to the user's phone number

        return Response({'message': result})


    def put(self, request):
        if request.method == 'PUT':
            serializer = KYCSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            documentType = serializer.validated_data.get('documentType')
            documentNumber = serializer.validated_data.get('documentNumber')
            documentURL = serializer.validated_data.get('documentURL')
            user_id = serializer.validated_data.get('user_id')

            # Create user in AWS Cognito
            cognito_client = boto3.client('cognito-idp', region_name=settings.AWS_COGNITO_REGION)
            response = cognito_client.admin_update_user_attributes(
                UserPoolId=settings.USER_POOL_ID,
                Username=user_id,
                UserAttributes=[
                    {
                        'Name': 'custom:id_document_number',
                        'Value': documentNumber
                    },
                    {
                        'Name': 'custom:id_document_type',
                        'Value': str(documentType)
                    },
                    {
                        'Name': 'custom:id_document_url',
                        'Value': documentURL
                    },
                ],
            )
            
            return Response({'message': 'User KYC details added.'})
        
# @csrf_exempt
# def verify_mfa_setup_challenge(session, sms_code="203250"):
#         cognito = boto3.client('cognito-idp', region_name=settings.AWS_COGNITO_REGION)
#         challenge_name = "SMS_MFA"
#         session = "AYABeKRf0cYrPJV6dhrxNytt8XgAHQABAAdTZXJ2aWNlABBDb2duaXRvVXNlclBvb2xzAAEAB2F3cy1rbXMAS2Fybjphd3M6a21zOnVzLWVhc3QtMjo0MTc1Njc5MDM0Njk6a2V5LzVjZDI0ZDRjLWVjNWItNGU4Ny05MGI2LTVkODdkOTZmY2RkMgC4AQIBAHjif3k0w30uAyP92ifoZ0jN6g50UW_KR0w9Vv2c_wlQAgHo0f1fZdmqW4F5OKyQ-JaKAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMLKghBB7QIXk3OTPNAgEQgDuCUXsI6pZrxH_Tkwyz-PObFcSQQU1xxR6jNN2Aq9j7S9CplW-hfKF4kz1Tg05DJb7Hi8GB58e5XB9Z_QIAAAAADAAAEAAAAAAAAAAAAAAAAAB2izGfd614JyVjPsR6DP-l_____wAAAAEAAAAAAAAAAAAAAAEAAAIA_BKsJRMCs3AKD62Hmk_WjbRBsIyqHK6Mt0h6ZCJsuANDWpfDJkmH3kYInBapwrQrOOhNW8IEstc7B_tzsXE7WMPYVkhjr2USuC8xT9V6F5m0GX-1UGps9nGBq0O-OnMKDM0TMnLjq3ai3r06IjV-am2tuTR6j9spG7Lgi0VpyAhHnMBLWCUIUZ5x_KXHvhZbMod6d7Q5PLE3yswZYyaEknCuAboTRqNMcTRvuML_93uhUepBbY6TO3ZNJ9I-NR6W-576cmriNhGW1J8LXMvtUNoDvnoOd_SK2H8eFumz2TohFfEowqARPGlK2r4j9DcZ6QQu9-1iS0ky3T3LaTxfK2K7quH7w4TpdQKzSQXWzqEf2o0NJjyL72pN2S2fodeXwH4W0PwMy8r-g1ollPsaNd-rQHBQEcxIXTA3tu7h6HP1e9Av-l7Y01LqPfKaDpBVzigB-aDZzglt4qc9-YnU2AXCQORM5UNgBA0wWmwmWPVBDaBLdSLzWLe2U20v1ESL50vhkj3zW20iI0prSZy3Ai7g-3JBoPXxJsb_RLV7Rd0Dk3L1qrL6FBDxlntNwB2BnkDRpifuJfWVOUaTSSk0Acet8smZP-Csnwk8fkWrbEECNJXu6lr6B7PCVZjEyJojCROVwu9W2_AlCvrB0Zyg8JvciB8DYC5jxcUekWTlSz-6ffl3s33BmY3PO4bQCbXk"
#         # response1 = cognito.respond_to_auth_challenge(
#         #     ClientId=settings.AWS_COGNITO_APP_CLIENT_ID,
#         #     ChallengeName=challenge_name,
#         #     Session=session,
#         #     ChallengeResponses={
#         #         'SMS_MFA_CODE': "675330",
#         #         'USERNAME': "+917355789992"
#         #     }
#         # )
#         # res = cognito.respond_to_auth_challenge(
#         #     ClientId=settings.AWS_COGNITO_APP_CLIENT_ID,
#         #     ChallengeName="SMS_MFA",
#         #     Session=session,
#         #     ChallengeResponses=response,
#         #     ClientMetadata={
#         #         'username': username
#         #     }
#         # )
#         print(">>>>>>>>>>>>>")
#         response = cognito.respond_to_auth_challenge(
#             ClientId=settings.AWS_COGNITO_APP_CLIENT_ID,
#             ChallengeName=challenge_name,
#             Session=session,
#             ChallengeResponses={
#                 'SMS_MFA_CODE': sms_code,
#                 'USERNAME': "8b61b7a0-9bbe-4bd0-903d-d2016b876cbf"
#             }
#         )
#         print("<<<<<<<<<<", response)
#         return Response({"RESULT": response})


# API class for User Login from AWS Cognito
class UserLoginView(RetrieveAPIView):
    permission_classes = [AllowAny,]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        password = serializer.validated_data.get('password')

        # Call AWS Cognito to get access token and refresh token
        try:
            client = boto3.client('cognito-idp', region_name=settings.AWS_COGNITO_REGION)
            print("<<<<<<<<<<<")
            # 'USER_SRP_AUTH'|'REFRESH_TOKEN_AUTH'|'REFRESH_TOKEN'|'CUSTOM_AUTH'|'USER_PASSWORD_AUTH'
            auth_response = client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': phone_number,
                    'PASSWORD': password
                },
                ClientId=settings.AWS_COGNITO_APP_CLIENT_ID
            )
            
        except client.exceptions.NotAuthorizedException as e:
            return Response({'error': 'Invalid phone number or password'})
        except Exception as e:
            return Response({'error': str(e)})

        # access_token = auth_response['AuthenticationResult']['AccessToken']
        # refresh_token = auth_response['AuthenticationResult']['RefreshToken']

        # # Store tokens in cookies or local storage
        # response = JsonResponse({'message': 'Logged in successfully',
        #                         'access_token': access_token,
        #                         'refresh_token': refresh_token})
        # response.set_cookie('access_token', access_token)
        # response.set_cookie('refresh_token', refresh_token)

        # Validate access token and get user details
        # user_response = client.get_user(AccessToken=access_token)
        # username = user_response['Username']
        # phone_number_verified = user_response['UserAttributes'][0]['Value']
        # Retrieve additional information from database based on user details
        # ...
        # print(user_response)

        return Response({'status': auth_response})


    def verify_mfa_setup_challenge(self, request):
        print(">>>>>>", request)
        # session,
        # sms_code,
        # challenge_name,
        # user_name
        cognito = boto3.client('cognito-idp', region_name=settings.AWS_COGNITO_REGION)
        # print(">>>>>>>>>>>>>")
        # response = cognito.respond_to_auth_challenge(
        #     ClientId=settings.AWS_COGNITO_APP_CLIENT_ID,
        #     ChallengeName=challenge_name,
        #     Session=session,
        #     ChallengeResponses={
        #         'SMS_MFA_CODE': sms_code,
        #         'USERNAME': user_name
        #     }
        # )
        # print("<<<<<<<<<<", response)
        return Response({"RESULT": 'response'})