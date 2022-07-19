from datetime import datetime
from django.contrib.auth import authenticate
from authentication.serializers import UserRegisterSerializer
from authentication.services.otp_service import OtpService
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from .models import PasswordReset, UserProfile


class Register(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        print(request.user)

        try:
            if request.user.is_anonymous:
                response_data = {"response_code": 0, "message":"you must be logged in as an admin to register a user 1", "data":""}
                return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)
            
            user = UserProfile.objects.filter(user = request.user)
            if not user.exists():
                response_data = {"response_code": 0, "messgae": "user does not exist", "data": ""}
                return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)
            
            if not user.first().role == 'admin':
                response_data = {"response_code": 0, "message":"you must be logged in as an admin to register a user 2", "data":""}
                return Response(data=response_data, status=status.HTTP_401_UNAUTHORIZED)
            
            email = request.data.get('email')
            phone = request.data.get('phone')
            serialized = UserRegisterSerializer(data=request.data)
            if not serialized.is_valid():
                response_data = {'response_code': 0, 'errors': serialized.errors, 'message': 'Bad requeset'}
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

            # check if email is not registered
            if UserProfile.objects.filter(user__email=email).exists():
                response_data = {'response_code': 0, 'message': 'Email address: {0}, is already registered. Please login or reset password'.format(email), "errer": ""}
                return Response(data=response_data,status=status.HTTP_409_CONFLICT)
            
            # check if phone number in not registered
            if UserProfile.objects.filter(phone=phone).exists():
                return Response(status=status.HTTP_409_CONFLICT, data={'response_code': 0, "message": "Phone number already registered", "error": ""})

            serialized.save()

            response = {
                "response_code": 1,
                "data": serialized.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            response = {
                "response_code": 0,
                "message": "user registration failed",
                "error": str(e)
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not UserProfile.objects.filter(user__email=email).exists():
                response_data = {
                    'response_code': 0,
                    'data': "login failed",
                    "message": "Email address not found. Please register"
                }
                return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

            user = authenticate(username=email, password=password)
            if user:
                # check if user is active
                profile = UserProfile.objects.get(user=user)
                if profile.is_active:
                    # Get token
                    token = Token.objects.get(user=user)
                    response_data = {
                        'response_code': 1,
                        'data': {
                            "uuid": profile.uuid,
                            "token": token.key,
                            "first_name": profile.user.first_name,
                            "last_name": profile.user.last_name,
                            "email": profile.user.email,
                            "phone": profile.phone,
                            "gender": profile.gender,
                            "profile_image": profile.profile_image,
                            "role": profile.role,
                            "city": profile.resident_city,
                            "country": profile.resident_country,
                        }
                    }
                    return Response(data=response_data, status=status.HTTP_200_OK)

                else:
                    response_data = {
                        'response_code': 0,
                        'data': "user account is not active",
                        'message': "your account is not active, contact admin for support"
                    }
                    return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

            response_data = {'response_code': 0, 'data': "login failed", "message": "Email or password is not valid"}
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            response = {
                'resonse_code': 0,
                'message': 'an error accured while trying to login',
                'error':str(e)
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SendOtpView(APIView):
     def post(self, request):
        try:
            email = request.data.get('email')
            if not UserProfile.objects.filter(user__email=email, is_active=True).exists():
                response = {
                    "response_code": 0,
                    "message": "User with this email does not exits"
                }
                return Response(data=response, status=status.HTTP_404_NOT_FOUND)

            otp = OtpService().generate({"email": email, })
            res = OtpService.send_email(self, email, otp)
            print(res)

            response = {
                'response_code': 1,
                'message': 'Email sent, check your email for an OTP to reset your password'
            }
            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'resonse_code': 0,
                'message': 'an error accured while sending otp',
                'error':str(e)
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResetPasswordView(APIView):
   
    def put(self, request):
        try:
            user_email = request.data.get('email', '').strip().lower()
            if not UserProfile.objects.filter(user__email=user_email, is_active=True).exists():
                response = {
                    "response_code": 0,
                    "message": "User with this email does not exits"
                }

                return Response(data=response, status=status.HTTP_404_NOT_FOUND)

            user_profile = UserProfile.objects.get(user__email=user_email, is_active=True)
            otp = request.data.get('otp', '').strip()

            if OtpService().verify(user_email, otp):

                user_profile.user.set_password(request.data.get('password', '').strip())
                user_profile.user.save()

                PasswordReset.objects.create(
                    user=user_profile,
                    is_used=True,
                    reset_key=otp,
                    salt=str(datetime.now())
                )

                response = {
                    'response_code': 0,
                    'message': 'Password reset successful'
                }
                return Response(data=response, status=status.HTTP_200_OK)

            response = {
                'response_code': 0,
                'message': 'Invalid OTP, Password reset failed'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            response = {
                'resonse_code': 0,
                'message': 'an error accured while resetting password',
                'error':str(e)
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
