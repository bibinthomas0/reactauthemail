from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from rest_framework import serializers
from accountt.models import CustomUser,Userdetails
from rest_framework_simplejwt.tokens import RefreshToken, Token,AccessToken
import random

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('password')
        
# class UserDetailsUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Userdetails
#         fields = ['profile_pic']
class UserDetailsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userdetails
        fields = ['profile_pic']
        
        
        
class OtpRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
class OtpResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField()


class AdminRegisterSerializer(serializers.ModelSerializer):
    userid = serializers.CharField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','username','name','email','dob','password','userid','is_superuser']
        extra_kwargs = {
            'password':{ 'write_only':True}
        }
    
    def create(self,validated_data):
        password = validated_data.pop('password',None)
        validated_data['userid'] = str(random.randint(100000, 999999))
        validated_data['is_superuser'] = True
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({"password": "password is not valid"})
        

class UserRegisterSerializer(serializers.ModelSerializer):
    userid = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','username','name','email','dob','password','userid']
        extra_kwargs = {
            'password':{ 'write_only':True}
        }
        
    
    def createsuperuser(self,validated_data):
        password = validated_data.pop('password',None)
        validated_data['userid'] = str(random.randint(100000, 999999))
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({"password": "password is not valid"})       
###################### ADMIN SIDE ####################

# class UserProfileSerializer(serializers.ModelSerializer):
#     # class Meta:
#     #     model = UserProfile
#     #     fields = ['profile_pic']
        
# class AdminUserSerializer(serializers.ModelSerializer):
#     User_Profile = UserProfileSerializer(required=False)

#     class Meta:
#         model = User
#         fields = ['id', 'first_name', 'last_name', 'phone_number', 'email', 'User_Profile','password','is_active','age']
#         extra_kwargs = {
#             'password':{ 'write_only':True},
#             'first_name': {'error_messages': {'required': 'Please provide the first name.'}},
#             'last_name': {'error_messages': {'required': 'Please provide the last name.'}},
#             'phone_number': {'error_messages': {'required': 'Please provide the phone number.'}},
#             'email': {'error_messages': {'required': 'Please provide the email address.'}},
#             'age': {'error_messages': {'required': 'Please provide the age'}},
            
            
#         }
    
   
    
    
#     def create(self, validated_data):
#         profile_data = validated_data.pop('User_Profile')
#         password = validated_data.pop('password',None)
#         print(password)
#         user_instance = self.Meta.model(**validated_data)
#         if password is not None:
#             user_instance.set_password(password)
#             user_instance.is_active=True
#             user_instance.save()
            
#         UserProfile.objects.create(user=user_instance, **profile_data)
#         return user_instance
    
# class UserUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['first_name', 'phone_number', 'email', 'is_active','age']

#     def update(self, instance, validated_data):
#         # Update user fields
#         instance.first_name = validated_data.get('first_name', instance.first_name)
    
#         instance.phone_number = validated_data.get('phone_number', instance.phone_number)
#         instance.email = validated_data.get('email', instance.email)
#         instance.age = validated_data.get('age', instance.age)
        
        
#         instance.is_active = validated_data.get('is_active', instance.is_active)
#         instance.save()
#         return instance