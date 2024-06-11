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
            
            #take the food info from api
            calories_per_100g = response_data[0].get('calories', 0)
            Protein_per_100g = response_data[0].get('protein_g', 0)
            fat_per_100g = response_data[0].get('fat_total_g', 0)
            carbohydrates_per_100g = response_data[0].get('carbohydrates_total_g', 0)
            
            #get the count depends en the grams take by the user
            calories = (calories_per_100g * grams) / 100
            fat = (fat_per_100g * grams) / 100
            protein = (Protein_per_100g * grams) / 100
            carbs = (carbohydrates_per_100g * grams) / 100
            
            #return the dictionary of all information
            return {
                'calories': calories,
                'protein': protein,
                'fat': fat,
                'carbs': carbs
            }
    except (requests.RequestException, IndexError, KeyError) as e:
        print(f"Error fetching calories: {e}")
    return {
        'calories':  0,
        'protein': 0,
        'fat': 0,
        'carbs': 0
    }

# Create your views here
@login_required
def nutriment_list(request):
    today = timezone.now().date()
    
    nutriments = Nutriment.objects.filter(user=request.user) # filter the request by only user information
    today_nutriments = nutriments.filter(date=today)
    
    
    daily_totals = nutriments.values('date').annotate(
        total_calories=Sum('calories'),
        total_protein=Sum('protein'),
        total_fat=Sum('fat'),
        total_carbs=Sum('carbs')
        ).order_by('-date') # get your food information only by your day
    
     
    total_calories = sum(n.calories for n in today_nutriments) #sum of calories the calories in the current day nutriments
    total_protein = sum(n.protein for n in today_nutriments) #sum of protein  in the current day nutriments
    total_fat = sum(n.fat for n in today_nutriments) #sum of fat in the current day nutriments
    total_carbs = sum(n.carbs for n in today_nutriments) #sum of carbs in the current day nutriments

    if request.method == "POST": #request POST
        form = NutrimentForm(request.POST)
        if form.is_valid():
            nutriment = form.save(commit=False)
            nutriment.user = request.user
            nutriment_info = fetch_calories(nutriment.name, nutriment.grams)
            nutriment.calories = nutriment_info['calories']
            nutriment.protein = nutriment_info['protein']
            nutriment.fat = nutriment_info['fat']
            nutriment.carbs = nutriment_info['carbs'] 
            nutriment.save()
            return redirect('nutriment_info')
    else:
        form = NutrimentForm()

    context = {
        'daily_totals': daily_totals,
        'nutriments': nutriments,
        'total_caloies': total_calories,
        'total_protein': total_protein,
        'total_fat': total_fat,
        'total_carbs': total_carbs,
        'form': form
    }
    return render(request, 'users/nutriment_list.html', context)


#view for logout function --> redirect to home page 
def logout_view(request):
    logout(request.user)
    return render(request, 'users/index.html')

def index_dash(request):
    return render(request, 'charts.html')
    