from django.db import models
from django.contrib.auth.models import User
from main.models import Toy

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.toy.name} × {self.quantity}"

    def total_price(self):
        return self.toy.price * self.quantity


