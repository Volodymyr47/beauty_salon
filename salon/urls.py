"""BeautySalon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from salon import views


urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('service/<str:service_name>/', views.one_service, name='one_service'),
    path('service/<str:service_name>/<int:specialist_id>/', views.one_service, name='one_service'),
    path('specialists/', views.specialists, name='specialists'),
    path('specialist/<int:specialist_id>/', views.one_specialist, name='one_specialist'),
    path('booking/<str:service_name>/<int:specialist_id>/', views.make_booking, name='make_booking'),
    path('booked/successful/<int:user_id>/', views.booking_success, name='booking_success'),
]
