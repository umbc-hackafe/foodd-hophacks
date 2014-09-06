import urllib
from foodd_project import settings
import json
from django.db import models
import django.contrib.auth.models as contrib_models
import foodd_main.barcode as barcodelib

class FooddUser(models.Model):
    UNITS_CHOICES = (
        ('M', 'Metric'),
        ('I', 'Standard American Imperial'),
        ('C', 'Cooking Units')
    )
    user = models.OneToOneField(contrib_models.User)
    units = models.CharField(max_length=1, choices=UNITS_CHOICES, default='C')

class Property(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=128)

    def __str__(self):
        return "Property: {}".format(self.name)

class Ingredient(models.Model):
    UNIT_CHOICES = (
        ('D', 'Discrete'),
        ('M', 'Mass'),
        ('V', 'Volume')
    )

    name = models.CharField(max_length=128, unique=True)
    unit = models.CharField(max_length=1, choices=UNIT_CHOICES)
    provides = models.ManyToManyField("self", blank=True)
    properties = models.ManyToManyField(Property, blank=True)

    def __str__(self):
        return "Ingredient: {}".format(self.name)

class Item(models.Model):
    ean = models.CharField(max_length=13, primary_key=True)
    ingredient = models.ForeignKey(Ingredient, null=True)
    size = models.IntegerField()
    description = models.CharField(max_length=128, blank=True)
    name = models.CharField(max_length=32)

    class NeedsIngredient(Exception): pass
    class NeedsData(Exception): pass

    class InvalidEAN(Exception): pass

    @classmethod
    def ensure_present(cls, ean):
        """Given an EAN (or non-sanitized form), ensure that it exists
in the database. This is accomplished by either finding it in the
database already, looking it up on the internet, or creating it blank.
If it is found, but lacks a parent ingredient, it raises
NeedsIngredient. If no data on the EAN could be found, it raises
NeedsData."""

        # Begin by sanitizing the EAN.
        ean = Item.to_ean(ean)

        try:
            item = cls.objects.get(pk=ean)
            return item
        except models.ObjectDoesNotExist:
            # If it could not be found, look it up.
            resp = urllib.request.urlopen(
                    'http://api.upcdatabase.org/json/{}/{}'.format(
                        settings.EAN_APIKEY, ean))
            response = json.loads(resp.read().decode('utf8'))

            if response['valid'] == "true":
                item = cls(
                        ean         = ean,
                        name        = response['itemname'],
                        description = response['description'],
                        size        = 0)
                item.save()
                return item
        return None

    @staticmethod
    def to_ean(barcode):
        return barcodelib.to_ean(barcode)

    def clean(self):
        super(Item, self).clean()

        self.ean = self.to_ean(self.ean)

    def __str__(self):
        return "Item: {}, {}".format(self.name, self.ean)

class Pantry(models.Model):
    owner = models.ForeignKey(FooddUser)
    name = models.CharField(max_length=32)
    members = models.ManyToManyField(FooddUser, through='PantryMembership', related_name='+')
    items = models.ManyToManyField(Item, through='PantryItem')

    def __str__(self):
        return "Pantry: owner: {}".format(self.owner.user.username)

class PantryMembership(models.Model):
    PANTRY_PERMISSIONS_CHOICES = (
        ('G', 'Guest'),
        ('M', 'Member'),
        ('O', 'Owner')
    )
    pantry = models.ForeignKey(Pantry)
    user = models.ForeignKey(FooddUser)
    permissions = models.CharField(max_length=1, choices=PANTRY_PERMISSIONS_CHOICES)

    def __str__(self):
        return "PantryMembership: Pantry: {}, Member: {}".format(self.pantry, self.user)

class PantryItem(models.Model):
    pantry = models.ForeignKey(Pantry)
    item = models.ForeignKey(Item)
    remaining = models.IntegerField(default=1)

    def __str__(self):
        return "Pantry Item: item: {}".format(self.item.name)

class Modifier(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return "Modifier: {}".format(self.name)

class Recipe(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    instructions = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='fromrecipe')
    preptime = models.IntegerField(blank=True)

    def __str__(self):
        return "Recipe: {}".format(self.name)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.FloatField()
    forproperties = models.ManyToManyField(Property, blank=True)
    required = models.BooleanField(default=True)
    modifiers = models.ManyToManyField(Modifier, blank=True)
    grouping = models.IntegerField(default=0)

    def __str__(self):
        return "RecipeIngredient: ingredient: {}, amount: {}".format(self.ingredient.name, self.amount)
