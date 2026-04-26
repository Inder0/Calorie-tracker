from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class FoodItem(models.Model):
    UNIT_CHOICES = [
        ("g", "Grams"),
        ("unit", "Unit (piece)"),
    ]
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="g")
    grams_per_unit = models.FloatField(null=True, blank=True)
    unit_name = models.CharField(
        max_length=20,
        blank=True,
        help_text="Display unit like cup, spoon, piece"
    )
    carbs = models.FloatField(help_text="per 100g")
    protein = models.FloatField(help_text="per 100g")
    fat = models.FloatField(help_text="per 100g")
    calories = models.FloatField(help_text="per 100g")

    def __str__(self):
        return self.name
    def get_measurement_display(self):
        if self.unit == "g":
            return "grams"

        if self.unit == "unit" and self.grams_per_unit:
            unit = self.unit_name if self.unit_name else "unit"
            return f"1 {unit} ≈ {int(self.grams_per_unit)}g"

        return ""

class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.FloatField(help_text="grams")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.food.name}"