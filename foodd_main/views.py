from django import http
from django import shortcuts

def home(request):
    shortcuts.render(request, "base.html")
