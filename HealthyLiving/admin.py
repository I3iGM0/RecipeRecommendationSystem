from django.contrib import admin
from .models import Recipe, RecentlyViewed

# Register your models here.
admin.site.register(Recipe)
admin.site.register(RecentlyViewed)
