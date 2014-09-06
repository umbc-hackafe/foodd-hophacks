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
    provides = models.ManyToManyField("self")
    properties = models.ManyToManyField(Property)

class Item(models.Model):
    ean = models.CharField(max_length=13, primary_key=True)
    ingredient = models.ForeignKey(Ingredient)
    size = models.IntegerField()
    description = models.CharField(max_length=128)

class PantryMembership(models.Model):
    PANTRY_PERMISSIONS_CHOICES = (
        ('G', 'Guest'),
        ('M', 'Member'),
        ('O', 'Owner')
    )
    user = models.ForeignKey(contrib_models.User)
    permissions = models.CharField(max_length=1, choices=PANTRY_PERMISSIONS_CHOICES)

class PantryItem(models.Model):
    item = models.ForeignKey(Item)
    remaining = models.IntegerField()

class Pantry(models.Model):
    owner = models.ForeignKey(contrib_models.User)
    members = models.ManyToManyField(contrib_models.User, through='PantryMembership')
    items = models.ManyToManyField(Item, through='PantryItem')

class Modifier(models.Model):
    name = models.CharField(max_length=32)

class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient)
    amount = models.FloatField()
    forproperties = models.ManyToManyField(Property)
    required = models.BooleanField(default=True)
    modifiers = models.ManyToManyField(Modifier)
    grouping = models.IntegerField(null=True)

class Recipe(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    instructions = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    preptime = models.IntegerField(null=True)
