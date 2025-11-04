from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', views.auth_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
]
