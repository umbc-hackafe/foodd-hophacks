from django.db import models
import django.contrib.auth.models as contrib_models

class Property(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128)

class Ingredient(models.Model):
    UNIT_CHOICES = (
        ('D', 'Discrete'),
        ('M', 'Mass'),
        ('V', 'Volume')
    )

    name = models.CharField(max_length=128)
    unit = models.CharField(max_length=1, choices=UNIT_CHOICES)
    provides = models.ManyToManyField("self", blank=True)
    properties = models.ManyToManyField(Property, blank=True)

class Item(models.Model):
    ean = models.CharField(max_length=13, primary_key=True)
    ingredient = models.ForeignKey(Ingredient)
    size = models.IntegerField()
    description = models.CharField(max_length=128)

class Pantry(models.Model):
    owner = models.ForeignKey(contrib_models.User)
    members = models.ManyToManyField(contrib_models.User, through='PantryMembership', related_name='+')
    items = models.ManyToManyField(Item, through='PantryItem')

class PantryMembership(models.Model):
    PANTRY_PERMISSIONS_CHOICES = (
        ('G', 'Guest'),
        ('M', 'Member'),
        ('O', 'Owner')
    )
    pantry = models.ForeignKey(Pantry)
    user = models.ForeignKey(contrib_models.User)
    permissions = models.CharField(max_length=1, choices=PANTRY_PERMISSIONS_CHOICES)

class PantryItem(models.Model):
    pantry = models.ForeignKey(Pantry)
    item = models.ForeignKey(Item)
    remaining = models.IntegerField(default=1)

class Modifier(models.Model):
    name = models.CharField(max_length=32)

class Recipe(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    instructions = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='fromrecipe')
    preptime = models.IntegerField(blank=True)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.FloatField()
    forproperties = models.ManyToManyField(Property, blank=True)
    required = models.BooleanField(default=True)
    modifiers = models.ManyToManyField(Modifier, blank=True)
    grouping = models.IntegerField(default=0)
