from django.urls import path
from . import views

urlpatterns = [
    path("weather/", views.get_weather, name="weather"),
    path("convert/", views.currency_convert, name="currency_convert"),
    path("quotes/", views.get_quotes, name="quotes"),
]
