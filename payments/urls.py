from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.payment_process, name='payment_process'),
    path('success/', views.payment_success, name='payment_success'),
]
