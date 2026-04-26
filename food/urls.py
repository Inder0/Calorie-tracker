from django.urls import path
from .views import DashboardView,AddFoodView,DeleteFoodView,get_food_unit,search_food

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("add-food/", AddFoodView.as_view(), name="add_food"),
    path("delete-food/<int:pk>/", DeleteFoodView.as_view(), name="delete_food"),
    path("get-food-unit/", get_food_unit, name="get_food_unit"),
    path("search-food/", search_food, name="search_food"),
]
