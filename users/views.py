from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.models import User
from .utils import get_food_info
from .forms import FoodForm
from .forms import NutrimentForm
from .models import Nutriment
from django.db.models import Sum
from django.utils import timezone
import requests

# Create your views here.

def home(request):
    return render(request, 'users/index.html')

def login_page(request):
    """login page via request method 'POST'"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        #check if the user with the provided name exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/users/login/')
        
        #Authenticate the user with the provided user name and password
        user = authenticate(username=username, password=password)
        
        if user is None:
            #display an error message if the authentication fail
            messages.error(request, "Invalid Password")
            return redirect('/users/login/')
        else:
            #login in the user and redirect to the home page
            login(request, user)
            return redirect('/users/food_info/')
        
    return render(request, 'authenticate/login.html') 


def register_page(request):
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Filter user by the username enter in the POST
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username already taken!")
            return redirect('/users/register/')
        
        #Create user in within the builtin class
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        user.set_password(password)
        user.save()
        
        messages.info(request, "Account created with success")
        return redirect('/users/login/')
    
    return render(request, 'authenticate/register.html')


def courses(request):
    '''nothing but just test'''
    return render (request, 'users/courses.html')

def index(request):
    return render (request, 'users/index.html')

def food_info_views(request):
    '''view to display some nutrition information'''
    food_info = None
    if request.method == 'POST':
        form = FoodForm(request.POST)  # create a form (class)  with the POST request
        if form.is_valid():
            food_item = form.cleaned_data['food_item'] #clean the data entered by the user
            food_info = get_food_info(food_item) #Fecth information from NINJA API
    else:
        form = FoodForm()
    
    return render(request, 'users/courses.html', {'form': form, 'food_info': food_info})


API_NINJAS_URL = 'https://api.api-ninjas.com/v1/nutrition'
API_NINJAS_HEADERS = {
    'X-Api-Key': '3dR8M9vuCA1x0BVHnBGiEg==C67Akb8Jsu2sQzFU'
}


def fetch_calories(food_name, grams):
    """counting view --- count your calories per day and display the history"""
    try:
        response = requests.get(API_NINJAS_URL, headers=API_NINJAS_HEADERS, params={'query': food_name})
        response.raise_for_status()
        response_data = response.json()

        if response_data:
            # Get the count for food information
            calories_and_macros = []
            calories_per_100g = response_data[0].get('calories', 0)
            Protein_per_100g = response_data[0].get('protein_g', 0)
            fat_per_100g = response_data[0].get('fat_total_g', 0)
            carbohydrates_per_100g = response_data[0].get('carbohydrates_total_g', 0)
            calories = (calories_per_100g * grams) / 100
            calories_and_macros.append(calories)
            fats = (fat_per_100g * grams) / 100
            calories_and_macros.append(fats)
            protein = (Protein_per_100g * grams) / 100
            calories_and_macros.append(protein)
            carbs = (carbohydrates_per_100g * grams) / 100
            calories_and_macros.append(carbs)
            return calories
    except (requests.RequestException, IndexError, KeyError) as e:
        print(f"Error fetching calories: {e}")
    return 0

# Create your views here
@login_required
def nutriment_list(request):
    today = timezone.now().date()
    
    nutriments = Nutriment.objects.filter(user=request.user) # filter the request by only user information
    today_nutriments = nutriments.filter(date=today)
    daily_totals = nutriments.values('date').annotate(total_calories=Sum('calories')).order_by('-date') # get your food information only by your day 
    total_calories = sum(n.calories for n in today_nutriments) #sum the calories in today nutriments

    if request.method == "POST":
        form = NutrimentForm(request.POST)
        if form.is_valid():
            nutriment = form.save(commit=False)
            nutriment.user = request.user
            nutriment.calories = fetch_calories(nutriment.name, nutriment.grams)
            if nutriment.calories is None:
                nutriment.calories = 0
            nutriment.save()
            return redirect('nutriment_info')
    else:
        form = NutrimentForm()

    context = {
        'daily_totals': daily_totals,
        'nutriments': nutriments,
        'total_calories': total_calories,
        'form': form
    }
    return render(request, 'users/Nutriment.html', context)



def logout_view(request):
    logout(request.user)
    return render(request, 'users/index.html')
