from django import forms

class FoodForm(forms.Form):
    food_item = forms.CharField(label="Food Item", max_length=100)
