from django.core.management.base import BaseCommand
import requests
from api.models import University

class Command(BaseCommand):
    help = "Fetch universities from Hipolabs API and save to DB"

    def add_arguments(self, parser):
        parser.add_argument(
            '--country', type=str, help='Country name to fetch universities for', required=True
        )

    def handle(self, *args, **options):
        country = options['country']
        url = f"http://universities.hipolabs.com/search?country={country}"
        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Failed to fetch data. Status: {response.status_code}"))
            return

        data = response.json()
        count = 0

        for uni in data:
            name = uni.get('name')
            if name:
                # Save or update to avoid duplicates
                obj, created = University.objects.get_or_create(
                    name=name,
                    country=country
                )
                if created:
                    count += 1

        self.stdout.write(self.style.SUCCESS(f"Added {count} universities for {country}"))
