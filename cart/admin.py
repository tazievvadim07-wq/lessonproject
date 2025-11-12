from django.contrib import admin
from .models import CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'toy', 'quantity', 'total_price')
    search_fields = ('user__username', 'toy__name')
