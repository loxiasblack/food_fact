from django import forms
from .models import Nutriment
 
#class for input from the user in the html
class FoodForm(forms.Form):
    food_item = forms.CharField(
        label="Food Item",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input-text'})
        )

#Nutriment Information for the count 
class NutrimentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','class': 'input-date'}),
        initial=forms.DateField().initial or None
    )
    class Meta:
        model = Nutriment
        fields = ['name', 'grams', 'date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-text'}),
            'grams': forms.NumberInput(attrs={'class': 'input-number'}),
        }
