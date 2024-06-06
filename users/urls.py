from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home, name="recipes"),
    path('login/', views.login_page, name="login_page"),
    path('home/', auth_views.LogoutView.as_view(next_page="home-landing"), name="logout"),
    path('register/', views.register_page, name="register"),
    path('courses/', views.courses, name="courses"),
    path('index/', views.index, name="index"),
    path('food_info/',views.food_info_views, name="food_info"),
    path('count/', views.nutriment_list, name="nutriment_info"),
]



