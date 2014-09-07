from django.core import exceptions
from foodd_main import models

def find_foodduser(request):
    if request.user.is_authenticated():
        try:
            foodduser = models.FooddUser.objects.get(user=request.user)
            return { 'foodduser': foodduser }
        except exceptions.ObjectDoesNotExist: pass

    return {}
