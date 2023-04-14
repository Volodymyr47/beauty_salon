from django.contrib.auth.views import LoginView
from django.urls import path, include
from user import views


urlpatterns = [
    path('', views.user_view, name='user_view'),
    path('registration/', views.register, name='register'),
    path('registration/', include('django.contrib.auth.urls')),
    path('pre_login/', views.pre_login, name='pre_login'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]
