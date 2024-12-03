from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),  
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bookings/', views.booking_list, name='booking_list'),  
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/create/<int:event_id>/', views.create_booking, name='create_booking'),
    path('bookings/cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),
]
