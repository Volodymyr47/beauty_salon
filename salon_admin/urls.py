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
from django.urls import path
from salon_admin import views

urlpatterns = [
    path('', views.main, name='adm_main'),
    path('bookings/', views.bookings, name='adm_bookings'),
    path('services/', views.services, name='adm_services'),
    path('services/<str:service_name>', views.service, name='adm_service'),
    path('specialists/', views.specialists, name='adm_specialists'),
    path('specialist/<int:specialist_id>', views.specialist, name='adm_specialist'),

]
