# main/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Toy, News

@receiver(post_save, sender=Toy)
def create_news_for_new_toy(sender, instance, created, **kwargs):
    if created:
        News.objects.create(
            title=f"Новая игрушка: {instance.name}",
            content=f"В наш ассортимент добавлена новая игрушка — {instance.name}! Скорее посмотрите подробности на главной странице."
        )
