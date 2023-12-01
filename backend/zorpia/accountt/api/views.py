from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accountt.models import CustomUser,Userdetails
from .serializers import UserRegisterSerializer,MyTokenObtainPairSerializer,UserSerializer,OtpResponseSerializer,AdminRegisterSerializer
from rest_framework.generics import ListCreateAPIView
import random
from rest_framework.exceptions import AuthenticationFailed,ParseError
from django.contrib.auth import authenticate
from .serializers import OtpRequestSerializer,UsernameSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from accountt.managers import CustomUserManager
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView

class getAccountsRoutes(APIView):
     def get(self, request, format=None):
        routes = [
        'api/accounts/login',
        'api/accounts/register',          ]
        return Response(routes)

class RegisterView(APIView):
    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE,)  

        content = {'Message':'User Registered Successfully'}
        return Response(content,status=status.HTTP_201_CREATED,)

class LoginView(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            password =request.data['password']
            print(email,password)
        except KeyError:
            content = 'All Fields Are Required'
            return Response(content,status=status.HTTP_400_BAD_REQUEST,)
        
        if not CustomUser.objects.filter(email=email).exists():
            content = 'Invalid Email Address'
            return Response(content,status=status.HTTP_404_NOT_FOUND,)
        
        if not CustomUser.objects.filter(email=email,is_blocked=True).exists():
            raise AuthenticationFailed('You are blocked by admin ! Please contact admin')
        
        user = authenticate(username=email, password=password)
        if user is None:
            content = "invalid password"
            return Response(content,status=status.HTTP_410_GONE)
        print("ggggggggg",user)
        refresh = RefreshToken.for_user(user)
        refresh["username"] = str(user.username)
       
        content = {
                     'refresh': str(refresh),
                     'access': str(refresh.access_token),
                     'isAdmin':user.is_superuser,
                }
        
        return Response(content,status=status.HTTP_200_OK)



class OtpRequestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if CustomUser.objects.filter(email=email).exists():
                    content ={'Message':'email already registered'}
                    return Response(content,status=status.HTTP_406_NOT_ACCEPTABLE,)
            else:
                custom_user_manager = CustomUserManager()
                content = custom_user_manager.send_otp_email(request, email)
                if content is not None:
                    otp = {"otp":content}
                    return Response(otp, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'An error occurred while sending the OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UsernameValidation(APIView):
    def post(self, request):
        serializer = UsernameSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            if CustomUser.objects.filter(username=username).exists():
                content = {'Message': 'Username already taken'}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                content = {'Message': 'Valid'}
                return Response(content, status=status.HTTP_202_ACCEPTED)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)  


class AdminRegisterView(APIView):
    def post(self,request):
        serializer = AdminRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE,)  

        content = {'Message':'User Registered Successfully'}
        return Response(content,status=status.HTTP_201_CREATED,)
