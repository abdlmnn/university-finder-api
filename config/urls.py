"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse
from django.http import HttpResponseRedirect
from api.views_frontend import home_view, favorites_view

urlpatterns = [
    path('admin/', admin.site.urls),    

    # API routes
    path('api/', include('api.urls')),
    
    path('', home_view, name='home'),

    # Social Auth and Account URLs
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', lambda request: HttpResponseRedirect('/')),
]
