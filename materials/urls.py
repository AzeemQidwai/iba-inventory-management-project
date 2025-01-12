from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_material, name='search_material'),  # Original search functionality
    path('forecast/', views.forecast_material, name='forecast_material'),  # New forecasting feature
    path('talk-with-data/', views.talk_with_data, name='talk_with_data'), 
]
