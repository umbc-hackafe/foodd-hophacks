from django.contrib import admin
from foodd_main.models import FooddUser, Property, Ingredient, Item, Pantry, PantryMembership, PantryItem, Modifier, Recipe, RecipeIngredient

class PantryItemInline(admin.TabularInline):
    model = PantryItem

class PantryAdmin(admin.ModelAdmin):
    inlines = [PantryItemInline,]

class PantryMembershipInline(admin.TabularInline):
    model = PantryMembership

class UserAdmin(admin.ModelAdmin):
    inlines = [PantryMembershipInline]

admin.site.register(FooddUser, UserAdmin)
admin.site.register(Property)
admin.site.register(Ingredient)
admin.site.register(Item)

admin.site.register(PantryItem)
admin.site.register(Pantry, PantryAdmin)

admin.site.register(PantryMembership)
admin.site.register(Modifier)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
