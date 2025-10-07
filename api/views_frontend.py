import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import University
from decouple import config

def home_view(request):
    return render(request, "home.html", {
        'google_api_key': config('GOOGLE_API_KEY'),
    })

@login_required
def university_view(request):
    # Define the specific countries to display
    available_countries = [
        "Philippines",
        "Japan",
        "India",
        "Australia",
        "Canada",
        "Singapore",
        "Thailand",
        "Saudi Arabia",
        "United Kingdom",
    ]

    selected_country = request.GET.get('country', 'Philippines')  # Default to Philippines
    search_query = request.GET.get('search', '').strip()
    universities = []
    loading = False
    error = None


    # Always load universities for the selected country (defaulting to Philippines)
    try:
        # Start with country filter
        queryset = University.objects.filter(country=selected_country)

        # Apply search filter if search query exists
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        # Order by name
        universities = queryset.order_by('name')
    except Exception as e:
        error = f"Error loading universities: {str(e)}"

    context = {
        'countries': available_countries,
        'selected_country': selected_country,
        'search_query': search_query,
        'universities': universities,
        'loading': loading,
        'error': error,
        'google_api_key': config('GOOGLE_API_KEY'),
        'google_map_id': os.getenv('GOOGLE_MAP_ID', ''),  # Pass Map ID to template
    }

    # Use different templates based on the URL
    if request.path == '/universities/':
        return render(request, "universities.html", context)
    else:
        return render(request, "home.html", context)


