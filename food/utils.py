from django.db.models import Sum, F, FloatField,DateTimeField, ExpressionWrapper,Case,When
from .models import FoodLog
from django.utils.timezone import localdate

def get_user_food_logs(user):
    today = localdate()
    quantity_in_grams = Case(
        When(food__unit="unit", then=F("quantity") * F("food__grams_per_unit")),
        default=F("quantity"),
        output_field=FloatField()
    )
    return (
        FoodLog.objects
        .filter(user=user,created_at__date=today)
        .select_related("food")
        .annotate(
            carbs_val=ExpressionWrapper(
                F("food__carbs") * quantity_in_grams / 100,
                output_field=FloatField()
            ),
            protein_val=ExpressionWrapper(
                F("food__protein") * quantity_in_grams / 100,
                output_field=FloatField()
            ),
            fat_val=ExpressionWrapper(
                F("food__fat") * quantity_in_grams / 100,
                output_field=FloatField()
            ),
            cal_val=ExpressionWrapper(
                F("food__calories") * quantity_in_grams /100,
                output_field=FloatField()
            ))
        .order_by("-created_at")
    )

def get_macro_totals(user):
    today = localdate()
    logs = FoodLog.objects.filter(user=user,created_at__date=today)
    quantity_in_grams = Case(
        When(food__unit="unit", then=F("quantity") * F("food__grams_per_unit")),
        default=F("quantity"),
        output_field=FloatField()
    )
    carbs_expr = ExpressionWrapper(
        F("food__carbs") * quantity_in_grams / 100,
        output_field=FloatField()
    )
    protein_expr = ExpressionWrapper(
        F("food__protein") * quantity_in_grams / 100,
        output_field=FloatField()
    )
    fat_expr = ExpressionWrapper(
        F("food__fat") * quantity_in_grams / 100,
        output_field=FloatField()
    )
    calories_expr = ExpressionWrapper(
        F("food__calories") * quantity_in_grams / 100,
        output_field=FloatField()
    )
    totals = logs.aggregate(
        total_carbs=Sum(carbs_expr),
        total_protein=Sum(protein_expr),
        total_fat=Sum(fat_expr),
        total_calories=Sum(calories_expr),
    )
    return {
        "total_carbs": totals["total_carbs"] or 0,
        "total_protein": totals["total_protein"] or 0,
        "total_fat": totals["total_fat"] or 0,
        "total_calories": totals["total_calories"] or 0,
    }

def get_nutrition_insights(totals, goal,user):
    insights = []

    calories = totals["total_calories"]
    protein = totals["total_protein"]
    fat = totals["total_fat"]
    carbs = totals["total_carbs"]

    if goal > 0:
        ratio = calories / goal

        if ratio < 0.7:
            insights.append(("You're eating too little", "text-blue-400"))

        elif ratio <= 1:
            insights.append(("You're within your calorie goal", "text-green-400"))

        else:
            insights.append(("You're over your calorie goal", "text-red-400"))

    protein_target = user.profile.weight * 1.5 if user.profile.weight else 70  # fallback default

    if protein < protein_target * 1:
        insights.append(("Protein intake is low — consider adding eggs/chicken", "text-yellow-400"))

    elif protein > protein_target * 1.8:
        insights.append(("Protein intake is high — good for muscle gain", "text-green-400"))

    if fat > (calories * 0.35) / 9:
        insights.append(("Fat intake is high — consider reducing oily foods", "text-red-400"))

    if carbs < (calories * 0.4) / 4:
        insights.append(("Carbs are low — energy levels may drop", "text-yellow-400"))

    return insights