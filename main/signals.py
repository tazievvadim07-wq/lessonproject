from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Toy, News
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=Toy)
def create_news_on_new_toy(sender, instance, created, **kwargs):
    if created:
        News.objects.create(
            title=f"Новая игрушка: {instance.name}",
            content=f"В магазин добавлена новая игрушка — {instance.name}! "
                    f"Цена: {instance.price}₸. {instance.description}"
        )

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
