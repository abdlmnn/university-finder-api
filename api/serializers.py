from rest_framework import serializers
from .models import University
from django.contrib.auth.models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from allauth.account import app_settings as allauth_account_settings

class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(
        required=allauth_account_settings.SIGNUP_FIELDS['email']['required']
    )

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name', 'country', 'lat', 'lng']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
