from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import University, FavoriteUniversity

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
                # Redirect back to the same page with the current country selection
                return redirect(f"{request.path}?country={selected_country}")
            except University.DoesNotExist:
                error = "University not found."
            except Exception as e:
                error = f"Error adding to favorites: {str(e)}"

    # Always load universities for the selected country (defaulting to Philippines)
    try:
        # Filter universities by selected country
        universities = University.objects.filter(country=selected_country).order_by('name')
    except Exception as e:
        error = f"Error loading universities: {str(e)}"

    context = {
        'countries': available_countries,
        'selected_country': selected_country,
        'universities': universities,
        'loading': loading,
        'error': error,
    }

    return render(request, "home.html", context)


@login_required
def favorites_view(request):
    favorites = FavoriteUniversity.objects.filter(user=request.user).select_related('university')
    context = {
        'favorites': favorites,
    }
    return render(request, "favorites.html", context)
