from django.urls import path
from .views import *

urlpatterns = [
    path('test/', test_view, name='test'),
    path('universities/', UniversityListView.as_view(), name='university-list'),
    path('search-university/', UniversitySearchView.as_view(), name='university-search'),
    path('favorites/', FavoriteUniversityListCreateView.as_view(), name='favorites'),
]
