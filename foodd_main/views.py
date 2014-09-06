from django import http
from django import shortcuts

def home(request):
    return shortcuts.render(request, "foodd_main/base.html")
