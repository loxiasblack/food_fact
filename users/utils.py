#!/usr/bin/python3
import requests

def get_food_info_admin(food_item):
    api_url = f'https://api.api-ninjas.com/v1/nutrition?query={food_item}'
    headers = {'X-Api-Key' : '3dR8M9vuCA1x0BVHnBGiEg==C67Akb8Jsu2sQzFU'}
    params = {
        'query': food_item.name
    }
    
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        data =  response.json()
        if data:
            food_data = data[0]
            food_item.calories = food_data[0].get('calories')
            food_item.protein = food_data[0].get('protein_g')
            food_item.carbohydrates = food_data[0].get('carbohydrates_total_g')
            food_item.fat = food_data[0].get('fat_total_g')
            food_item.save()
            return True
    else:
        return None


def get_food_info(food_item):
    api_url = f'https://api.api-ninjas.com/v1/nutrition?query={food_item}'
    headers = {'X-Api-Key' : '3dR8M9vuCA1x0BVHnBGiEg==C67Akb8Jsu2sQzFU'}

    
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data =  response.json()
        return data
    else:
        return None
