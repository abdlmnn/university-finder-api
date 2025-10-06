from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import University, FavoriteUniversity
from decouple import config

@login_required
def home_view(request):
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

    # Handle adding to favorites
    if request.method == 'POST':
        university_id = request.POST.get('university_id')
        if university_id:
            try:
                university = University.objects.get(id=university_id)
                FavoriteUniversity.objects.get_or_create(
                    user=request.user,
                    university=university
                )
                # Redirect back to the same page with the current country selection and search
                redirect_url = f"{request.path}?country={selected_country}"
                if search_query:
                    redirect_url += f"&search={search_query}"
                return redirect(redirect_url)
            except University.DoesNotExist:
                error = "University not found."
            except Exception as e:
                error = f"Error adding to favorites: {str(e)}"

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
    }

    # Use different templates based on the URL
    if request.path == '/universities/':
        return render(request, "universities.html", context)
    else:
        return render(request, "home.html", context)


@login_required
def favorites_view(request):
    favorites = FavoriteUniversity.objects.filter(user=request.user).select_related('university')
    context = {
        'favorites': favorites,
    }
    return render(request, "favorites.html", context)
