from foodd_main import models

def find_foodduser(request):
    if request.user.is_authenticated():
        foodduser = models.FooddUser.objects.get(user=request.user)
        return { 'foodduser': foodduser }
