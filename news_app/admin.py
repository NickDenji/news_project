from django.contrib import admin
from .models import User, Publisher, Article, Newsletter

# Register your models here.

admin.site.register(User)
admin.site.register(Publisher)
admin.site.register(Article)
admin.site.register(Newsletter)
