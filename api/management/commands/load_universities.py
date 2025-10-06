from django.core.management.base import BaseCommand
import requests
from api.models import University

class Command(BaseCommand):
    help = 'Load universities from Hipolabs API for specified countries'

    def add_arguments(self, parser):
        parser.add_argument(
            '--countries',
            nargs='+',
            type=str,
            help='List of countries to load universities for',
            default=[
                "Philippines", "Japan", "India", "Australia",
                "Canada", "Singapore", "Thailand", "Saudi Arabia", "United Kingdom"
            ]
        )

    def handle(self, *args, **options):
        countries = options['countries']

        for country in countries:
            self.stdout.write(f'Loading universities for {country}...')

            # Fetch from Hipolabs API
            url = f"http://universities.hipolabs.com/search?country={country}"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
            except requests.RequestException as e:
                self.stderr.write(f'Error fetching data for {country}: {e}')
                continue

            universities_added = 0
            for uni in data:
                name = uni.get("name")
                if name:
                    # Get coordinates for the university
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

                    if created:
                        universities_added += 1

            self.stdout.write(f'Added {universities_added} universities for {country}')

        total_universities = University.objects.count()
        self.stdout.write(f'Total universities in database: {total_universities}')