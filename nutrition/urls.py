from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_info_views, name='food_views')
]

