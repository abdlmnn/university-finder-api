from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import requests
from decouple import config
from .models import University, FavoriteUniversity
from .serializers import UniversitySerializer, FavoriteUniversitySerializer
from rest_framework.permissions import IsAuthenticated

GOOGLE_API_KEY = config("GOOGLE_API_KEY")


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })


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
# 3. Get university locations for map display
# --------------------------
class UniversityLocationsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        country = request.query_params.get('country', 'Philippines')

        # Get universities from database
        universities = University.objects.filter(country__iexact=country)

        locations = []
        for uni in universities[:20]:  # Limit to 20 for performance
            # Try to get coordinates from Places API
            url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
            params = {
                "input": f"{uni.name} {uni.country}",
                "inputtype": "textquery",
                "fields": "geometry,name,formatted_address,place_id",
                "key": GOOGLE_API_KEY
            }

            try:
                response = requests.get(url, params=params, timeout=5)
                response.raise_for_status()
                data = response.json()

                if 'candidates' in data and len(data['candidates']) > 0:
                    candidate = data['candidates'][0]
                    location_data = {
                        "id": uni.id,
                        "name": uni.name,
                        "country": uni.country,
                        "lat": candidate['geometry']['location']['lat'],
                        "lng": candidate['geometry']['location']['lng'],
                        "address": candidate.get('formatted_address', ''),
                        "place_id": candidate.get('place_id', '')
                    }
                    locations.append(location_data)
                else:
                    # Use stored coordinates if available, or skip
                    if uni.lat and uni.lng:
                        locations.append({
                            "id": uni.id,
                            "name": uni.name,
                            "country": uni.country,
                            "lat": uni.lat,
                            "lng": uni.lng,
                            "address": f"{uni.name}, {uni.country}",
                            "place_id": ""
                        })

            except requests.RequestException:
                # Use stored coordinates if API fails
                if uni.lat and uni.lng:
                    locations.append({
                        "id": uni.id,
                        "name": uni.name,
                        "country": uni.country,
                        "lat": uni.lat,
                        "lng": uni.lng,
                        "address": f"{uni.name}, {uni.country}",
                        "place_id": ""
                    })
                continue

        return Response(locations)


# --------------------------
# 4. Favorite universities
# --------------------------
class FavoriteUniversityListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteUniversitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteUniversity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        university_data = self.request.data.get("university")
        if not university_data:
            raise ValueError("Missing 'university' data")

        # Save or get university
        uni_obj, created = University.objects.get_or_create(
            name=university_data.get("name"),
            country=university_data.get("country", "")
        )
        serializer.save(user=self.request.user, university=uni_obj)
