from django.shortcuts import render
from .forms import FoodForm
from .utils import get_food_info
# Create your views here.

def food_info_views(request):
    food_info = None
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            food_item = form.cleaned_data['food_item']
            food_info = get_food_info(food_item)
            print(food_info)
    else:
        form = FoodForm()
    
    return render(request, 'users/food_info.html', {'form': form, 'food_info': food_info})
