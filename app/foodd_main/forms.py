from django.forms import ModelForm, PasswordInput
from django.contrib import auth
from foodd_main import models

class ItemForm(ModelForm):
    class Meta:
        model = models.Item

class FooddUserForm(ModelForm):
    class Meta:
        model = models.FooddUser
        fields = ["units"]

class UserForm(ModelForm):
    class Meta:
        model = auth.models.User
        fields = ["username", "password", "first_name", "last_name", "email"]

class PantryForm(ModelForm):
    class Meta:
        model = models.Pantry
        fields = ["name"]
