from django.urls import path
from . import views
from cart.models import CartItem

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', views.auth_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('toy/<int:toy_id>/', views.buy_now, name='buy_now'),
    path('cart/add/<int:toy_id>/', views.add_to_cart, name='add_to_cart'),
    
    
]
