from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import requests
from decouple import config
from .models import University, FavoriteUniversity
from .serializers import UniversitySerializer, FavoriteUniversitySerializer

GOOGLE_API_KEY = config("GOOGLE_API_KEY")


# --------------------------
# 0. Test view
# --------------------------
def test_view(request):
    return JsonResponse({"message": "API is working!"})


# --------------------------
# 1. List all universities (from DB or Hipolabs API)
# --------------------------
class UniversityListView(generics.ListAPIView):
    serializer_class = UniversitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        country = self.request.query_params.get('country', None)

        if not country:
            return University.objects.all()

        # Check if there are universities stored for this country
        qs = University.objects.filter(country__iexact=country)
        if qs.exists():
            return qs

        # If not, fetch from Hipolabs API
        url = f"http://universities.hipolabs.com/search?country={country}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            return University.objects.none()  # Return empty queryset if API fails

        # Optionally save to DB for caching/favorites
        universities = []
        for uni in data:
            name = uni.get("name")
            if name:
                obj, created = University.objects.get_or_create(
                    name=name,
                    country=country
                )
                universities.append(obj)

        return universities



# --------------------------
# 2. Search university by name (Google Places API)
# --------------------------
class UniversitySearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({"error": "Missing 'name' parameter"}, status=400)

        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            "input": name,
            "inputtype": "textquery",
            "fields": "geometry,name,formatted_address",
            "key": GOOGLE_API_KEY
        }

        response = requests.get(url, params=params).json()

        if 'candidates' in response and len(response['candidates']) > 0:
            candidate = response['candidates'][0]
            data = {
                "name": candidate.get("name"),
                "address": candidate.get("formatted_address"),
                "lat": candidate['geometry']['location']['lat'],
                "lng": candidate['geometry']['location']['lng']
            }
            return Response(data)

        return Response({"error": "University not found"}, status=404)


# --------------------------
# 3. Favorite universities
# --------------------------
class FavoriteUniversityListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteUniversitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteUniversity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        university_id = self.request.data.get('university_id')
        if university_id:
            serializer.save(user=self.request.user, university_id=university_id)
