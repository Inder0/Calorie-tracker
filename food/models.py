from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    carbs = models.FloatField(help_text="per 100g")
    protein = models.FloatField(help_text="per 100g")
    fat = models.FloatField(help_text="per 100g")
    calories = models.FloatField(help_text="per 100g")

    def __str__(self):
        return self.name


class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.FloatField(help_text="grams")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.food.name}"