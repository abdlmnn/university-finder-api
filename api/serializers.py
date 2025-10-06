from rest_framework import serializers
from .models import University, FavoriteUniversity
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

class FavoriteUniversitySerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)

    class Meta:
        model = FavoriteUniversity
        fields = ['id', 'user', 'university', 'added_at']

        def create(self, validated_data):
            # Extract nested university data
            university_data = validated_data.pop('university')
            university_obj, _ = University.objects.get_or_create(
                name=university_data.get('name'),
                defaults={
                    'country': university_data.get('country', ''),
                    'lat': university_data.get('lat', None),
                    'lng': university_data.get('lng', None),
                }
            )
            # Create favorite
            favorite = FavoriteUniversity.objects.create(
                user=self.context['request'].user,
                university=university_obj
            )
            return favorite

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
