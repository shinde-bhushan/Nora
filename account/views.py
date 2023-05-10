import boto3
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import boto3

def home(request):
    return HttpResponse("HEY")

cognito = boto3.client('cognito-idp', region_name=settings.AWS_COGNITO_REGION)
@csrf_exempt
def verify_signup_otp(request):
    phone_number = request.POST.get('phone_number', '735578999')
    verification_code = request.POST.get('verification_code', '734610')
    response = cognito.confirm_sign_up(
        ClientId=settings.AWS_COGNITO_APP_CLIENT_ID,
        Username=phone_number,
        ConfirmationCode=verification_code
    )
    print(response['ResponseMetadata']['HTTPStatusCode'] == 200)



@csrf_exempt
def signup(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', '735578999')
        password = request.POST.get('password', 'Pass@123')
        name = request.POST.get('name', 'Piyush')
        email = request.POST.get('email', 'piyush.khare8@gmail.com')
        user_model = get_user_model()

        try:
            user = user_model.objects.create_user(phone_number=phone_number,
                                                  password=password,
                                                  name=name,
                                                  email=email)
            print("<<<<")
        except Exception as e:
            print("USER EXCEPT")
            return JsonResponse({'error': str(e)}, status=400)

        try:
            client = boto3.client('cognito-idp',
                              region_name=settings.AWS_COGNITO_REGION,
                              aws_access_key_id=settings.AWS_ACCESS_ID,
                              aws_secret_access_key=settings.AWS_SECRET_KEY)
            response = client.sign_up(ClientId=settings.AWS_COGNITO_APP_CLIENT_ID,
                                        Username=phone_number,
                                        Password=password,
                                        UserAttributes=[{'Name': 'name', 'Value': name},
                                                       {'Name': 'email', 'Value': email}],  
                                        ValidationData=[{'Name': 'email', 'Value': email}])
            print("AWS ACCESSED", response)
        except Exception as e:
            print("AWS EXCEPT")
            user.delete()
            return JsonResponse({'error': str(e)}, status=400)

        user.set_password(make_password(password))
        print("USER SAVE IN DB")
        user.save()

        return JsonResponse({'success': True, 'response': response['UserSub']}, status=201)
def verify_mfa_setup_challenge(session, sms_code):
    response = cognito.respond_to_auth_challenge(
        ClientId=settings.AWS_COGNITO_APP_CLIENT_ID,
        ChallengeName='MFA_SETUP',
        Session=session,
        ChallengeResponses={
            'SMS_MFA_CODE': sms_code,
            'USERNAME': 'piyush.khare8@gmail.com'
        }
    )
    return response

@csrf_exempt
def login(request):
    # Get user phone number and password from request
    phone_number = request.POST.get('phone_number', '7355789992')
    password = request.POST.get('password', 'Pass@123')

    # Call AWS Cognito to get access token and refresh token
    try:
        client = boto3.client('cognito-idp', region_name=settings.AWS_COGNITO_REGION)

        auth_response = client.admin_initiate_auth(
            UserPoolId=settings.USER_POOL_ID,
            ClientId=settings.AWS_COGNITO_APP_CLIENT_ID,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': phone_number,
                'PASSWORD': password
            }
        )
        print(">>>>>>>>>>", auth_response)
        response = verify_mfa_setup_challenge(auth_response['Session'], sms_code='140306')
    except client.exceptions.NotAuthorizedException as e:
        return JsonResponse({'error': 'Invalid phone number or password'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    access_token = auth_response['AuthenticationResult']['AccessToken']
    refresh_token = auth_response['AuthenticationResult']['RefreshToken']

    # Store tokens in cookies or local storage
    response = JsonResponse({'message': 'Logged in successfully',
                             'access_token': access_token,
                             'refresh_token': refresh_token})
    # response.set_cookie('access_token', access_token)
    # response.set_cookie('refresh_token', refresh_token)

    # Validate access token and get user details
    user_response = client.get_user(AccessToken=access_token)
    username = user_response['Username']
    phone_number_verified = user_response['UserAttributes'][0]['Value']
    # Retrieve additional information from database based on user details
    # ...
    print(user_response)

    return response