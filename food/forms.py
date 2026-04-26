from django import forms
from .models import FoodLog, FoodItem


class FoodLogForm(forms.ModelForm):
    class Meta:
        model = FoodLog
        fields = ["food", "quantity"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["food"].queryset = FoodItem.objects.all()
        self.fields["quantity"].widget.attrs.update({
            "placeholder": "Grams or Units",
            "class": "w-full bg-gray-700 p-3 rounded-lg outline-none focus:ring-2 focus:ring-blue-500",
        })
        