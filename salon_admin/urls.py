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
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('login/', LoginView.as_view(template_name='salon_admin/login.html'), name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('bookings/', views.bookings, name='adm_bookings'),
    path('services/', views.services, name='adm_services'),
    path('service/<int:service_id>/', views.one_service, name='adm_service'),
    path('specialists/', views.specialists, name='adm_specialists'),
    path('specialist/<int:specialist_id>/', views.one_specialist, name='adm_specialist'),

]
