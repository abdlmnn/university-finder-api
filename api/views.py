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
                # Try to get coordinates for the university
                state_province = uni.get("state-province", "")
                search_query = f"{name} {state_province} {country}".strip()

                # Get coordinates using Nominatim
                lat, lng = None, None
                try:
                    nominatim_url = "https://nominatim.openstreetmap.org/search"
                    params = {
                        "q": search_query,
                        "format": "json",
                        "limit": 1,
                        "addressdetails": 1
                    }
                    response = requests.get(nominatim_url, params=params, headers={
                        'User-Agent': 'UniversityFinder/1.0'
                    }, timeout=5)
                    response.raise_for_status()
                    nominatim_data = response.json()

                    if nominatim_data:
                        lat = float(nominatim_data[0].get("lat"))
                        lng = float(nominatim_data[0].get("lon"))
                except:
                    pass  # Continue without coordinates if geocoding fails

                obj, created = University.objects.get_or_create(
                    name=name,
                    country=country,
                    defaults={'lat': lat, 'lng': lng}
                )

                # Update coordinates if they weren't set before
                if created and lat and lng:
                    pass  # Already set in defaults
                elif not obj.lat and lat and lng:
                    obj.lat = lat
                    obj.lng = lng
                    obj.save()

                universities.append(obj)

        return universities

# --------------------------
# 2. Search university by name (OpenStreetMap Nominatim API)
# --------------------------
class UniversitySearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({"error": "Missing 'name' parameter"}, status=400)

        # Use OpenStreetMap Nominatim API (free, no API key needed)
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": name,
            "format": "json",
            "limit": 1,
            "addressdetails": 1,
            "extratags": 1
        }

        try:
            response = requests.get(url, params=params, headers={
                'User-Agent': 'UniversityFinder/1.0'  # Required by Nominatim
            }, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data and len(data) > 0:
                result = data[0]
                return Response({
                    "name": result.get("display_name", "").split(",")[0],  # Get just the name part
                    "address": result.get("display_name"),
                    "lat": float(result.get("lat")),
                    "lng": float(result.get("lon"))
                })

        except requests.RequestException as e:
            return Response({"error": f"Geocoding service unavailable: {str(e)}"}, status=503)

        return Response({"error": "University not found"}, status=404)


# --------------------------
# 3. Get university locations for map display (OpenStreetMap Nominatim)
# --------------------------
class UniversityLocationsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        country = request.query_params.get('country', 'Philippines')

        # Get universities from database
        universities = University.objects.filter(country__iexact=country)

        locations = []
        for uni in universities[:20]:  # Limit to 20 for performance
            # Try to get coordinates from OpenStreetMap Nominatim (free)
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": f"{uni.name} {uni.country}",
                "format": "json",
                "limit": 1,
                "addressdetails": 1
            }

            try:
                response = requests.get(url, params=params, headers={
                    'User-Agent': 'UniversityFinder/1.0'  # Required by Nominatim
                }, timeout=5)
                response.raise_for_status()
                data = response.json()

                if data and len(data) > 0:
                    result = data[0]
                    location_data = {
                        "id": uni.id,
                        "name": uni.name,
                        "country": uni.country,
                        "lat": float(result.get("lat")),
                        "lng": float(result.get("lon")),
                        "address": result.get("display_name", f"{uni.name}, {uni.country}"),
                        "place_id": result.get("place_id", "")
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
