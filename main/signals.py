from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Toy, News

@receiver(post_save, sender=Toy)
def create_news_on_new_toy(sender, instance, created, **kwargs):
    if created:
        News.objects.create(
            title=f"Новая игрушка: {instance.name}",
            content=f"В магазин добавлена новая игрушка — {instance.name}! "
                    f"Цена: {instance.price}₸. {instance.description}"
        )
