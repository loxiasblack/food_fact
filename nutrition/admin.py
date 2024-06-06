# nutrition/admin.py
from django.contrib import admin
from .models import FoodItem
from .utils import get_food_info_admin

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'protein', 'carbohydrates', 'fat')
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        # Call the original save method to ensure the object is saved
        super().save_model(request, obj, form, change)
        
        # Fetch and update nutrition information
        if get_food_info_admin(obj):
            self.message_user(request, f"Updated {obj.name} with nutritional information.")
        else:
            self.message_user(request, f"Failed to update {obj.name} with nutritional information.", level='error')
