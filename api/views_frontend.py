from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, "home.html")


@login_required
def favorites_view(request):
    return render(request, "favorites.html")
