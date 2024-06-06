from django import forms
from .models import Nutriment

class FoodForm(forms.Form):
    food_item = forms.CharField(label="Food Item", max_length=100)


class NutrimentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget, initial=forms.DateField().initial or None)

    class Meta:
        model = Nutriment
        fields = ['name', 'grams', 'date']
