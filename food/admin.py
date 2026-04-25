from django.contrib import admin
from .models import FoodItem,FoodLog
# Register your models here.
admin.site.register(FoodItem)
admin.site.register(FoodLog)