from django import ModelForm
import models

class ItemForm(ModelForm):
    class Meta:
        model = models.Item

class UserForm(ModelForm):
    class Meta:
        model = models.FooddUser

class PantryForm(ModelForm):
    class Meta:
        model = models.Pantry
