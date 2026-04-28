from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import get_macro_totals, get_user_food_logs,get_nutrition_insights
from .forms import FoodLogForm
from django.views.generic import FormView, View
from django.urls import reverse_lazy 
from .models import FoodLog,FoodItem
from django.http import HttpResponse
from django.core.paginator import Paginator

# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "food/dashboard.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if request.headers.get("HX-Request"):
            return render(request, "food/partials/dashboard_update.html", context)

        return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        totals = get_macro_totals(user)
        logs = get_user_food_logs(user)
        insights = get_nutrition_insights(
            totals,
            user.profile.daily_calorie_goal,
            self.request.user
        )
        total_macros = totals['total_carbs'] + totals['total_protein'] + totals['total_fat']
        context["carbs_pct"] = (totals['total_carbs'] / total_macros * 100) if total_macros else 0
        context["protein_pct"] = (totals['total_protein'] / total_macros * 100) if total_macros else 0
        context["fat_pct"] = (totals['total_fat'] / total_macros * 100) if total_macros else 0
        paginator = Paginator(logs, 10)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["insights"] = insights
        context["form"] = FoodLogForm()
        context.update(totals)
        context["logs"] = page_obj
        context['page_obj']=page_obj
        context["goal"] = user.profile.daily_calorie_goal

        return context
    
class AddFoodView(LoginRequiredMixin, FormView):
    form_class = FoodLogForm
    
    def form_valid(self, form):
        food_log = form.save(commit=False)
        food_log.user = self.request.user
        food_log.save()
        return self.render_dashboard_partial(form=FoodLogForm())

    def form_invalid(self, form):     
        return self.render_dashboard_partial(form=form)

    def render_dashboard_partial(self, form):
        user = self.request.user
        totals = get_macro_totals(user)
        logs = get_user_food_logs(user)
        insights = get_nutrition_insights(totals, user.profile.daily_calorie_goal, user=user)
        
        paginator = Paginator(logs, 10)
        page_obj = paginator.get_page(self.request.GET.get("page"))
        total_macros = totals['total_carbs'] + totals['total_protein'] + totals['total_fat']
        context = {
            **totals,
            "logs": page_obj,
            "page_obj": page_obj,
            "goal": user.profile.daily_calorie_goal,
            "form": form,
            "insights": insights,
        }
        context["carbs_pct"] = (totals['total_carbs'] / total_macros * 100) if total_macros else 0
        context["protein_pct"] = (totals['total_protein'] / total_macros * 100) if total_macros else 0
        context["fat_pct"] = (totals['total_fat'] / total_macros * 100) if total_macros else 0

        return render(self.request, "food/partials/dashboard_update.html", context)
    
class DeleteFoodView(LoginRequiredMixin, View):

    def post(self, request, pk):
        log = get_object_or_404(FoodLog, pk=pk, user=request.user)
        log.delete()

        logs = get_user_food_logs(request.user)
        totals = get_macro_totals(request.user)
        insights = get_nutrition_insights(
            totals,
            request.user.profile.daily_calorie_goal,
            user=self.request.user
        )
        paginator = Paginator(logs, 10)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        total_macros = totals['total_carbs'] + totals['total_protein'] + totals['total_fat']

        context = {
            **totals,
            "goal": request.user.profile.daily_calorie_goal,
            "form": FoodLogForm(),
            "insights": insights
        }
        context["logs"] = page_obj
        context['page_obj']=page_obj
        context["carbs_pct"] = (totals['total_carbs'] / total_macros * 100) if total_macros else 0
        context["protein_pct"] = (totals['total_protein'] / total_macros * 100) if total_macros else 0
        context["fat_pct"] = (totals['total_fat'] / total_macros * 100) if total_macros else 0

        return render(request, "food/partials/dashboard_update.html", context)

def get_food_unit(request):
    food_id = request.GET.get("food")
    if not food_id:
        return HttpResponse("Enter quantity")
    try:
        food = FoodItem.objects.get(id=food_id)
    except FoodItem.DoesNotExist:
        return HttpResponse("Enter quantity")
    if food.unit == "unit":
        return HttpResponse("Enter number of items (e.g., eggs)")
    else:
        return HttpResponse("Enter grams")
    
def search_food(request):
    query = request.GET.get("search", "")

    foods = FoodItem.objects.filter(name__icontains=query)[:10]

    for food in foods:
        if food.unit == "unit":
            food.unit_label = "Number of items"
        else:
            food.unit_label = "Grams"

    return render(request, "food/partials/food_search_results.html", {
        "foods": foods
    })