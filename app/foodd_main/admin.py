from django.contrib import admin
from foodd_main.models import Property, Ingredient, Item, Pantry, PantryMembership, PantryItem, Modifier, Recipe, RecipeIngredient

admin.site.register(Property)
admin.site.register(Ingredient)
admin.site.register(Item)
admin.site.register(Pantry)
admin.site.register(PantryMembership)
admin.site.register(PantryItem)
admin.site.register(Modifier)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
