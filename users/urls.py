from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *

urlpatterns=[
    path('login/',CustomLoginView.as_view(template_name='users/login.html'),name='login'),
    path('register/',register,name='register'),
    path('logout/',logout_view,name='logout'),
    path("profile/", ProfileUpdateView.as_view(), name="profile")
]