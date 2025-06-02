from django.urls import path
from . import views

urlpatterns = (
    path('', views.search_flights, name='search_flights'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('find-booking/', views.find_booking, name='find_booking'),
)
