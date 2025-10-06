from rest_framework import serializers
from .models import University, FavoriteUniversity
from django.contrib.auth.models import User

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
