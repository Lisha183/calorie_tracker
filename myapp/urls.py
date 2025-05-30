from django.urls import path
from .views import (
    HomePageView, LoginPage, LogOutPage, select_food, add_food,
    RegisterPage, ProfilePage, update_food, delete_food, add_meal
)
from . import views


urlpatterns = [
    path('', HomePageView, name='home'),
    path('login/', LoginPage, name='login'),
    path('logout/', LogOutPage, name='logout'),
    path('select_food/', select_food, name='select_food'),
    path('add_food/', add_food, name='add_food'),
    path('add_meal/<int:food_id>/', add_meal, name='add_meal'), 
    path('update_food/<str:pk>/', update_food, name='update_food'),
    path('delete_food/<str:pk>/', delete_food, name='delete_food'),
    path('register/', RegisterPage, name='register'),
    path('profile/', ProfilePage, name='profile'),
    path('test-login/', views.test_view, name='test_login'),
]
