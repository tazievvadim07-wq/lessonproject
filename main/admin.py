from django.contrib import admin
from .models import Toy, Tag, News

admin.site.register(Toy)
admin.site.register(Tag)
admin.site.register(News)