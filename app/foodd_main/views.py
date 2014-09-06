from django import http
from django.views import generic
from django import shortcuts
from django.core import serializers
import foodd_main.models as models
import json
import os
import urllib

EAN_APIKEY = os.getenv("FOODD_EANDATABASE_KEY")

class HomeView(generic.TemplateView):
    template_name = "foodd_main/home.html"

class IngredientsView(generic.ListView):
    template_name = "foodd_main/ingredients.html"
    context_object_name = "ingredients"
    queryset = models.Ingredient.objects.all()

class IngredientView(generic.DetailView):
    context_object_name = "ingredient"
    template_name = "foodd_main/ingredient.html"

    def get_queryset(self):
        return shortcuts.get_object_or_404(models.Ingredient, name__iexact=self.args[0])

    def get_context_data(self, **kwargs):
        context = super(IngredientView, self).get_context_data(**kwargs)
        return context

def ean_info(request, ean):
    return http.HttpResponse(status=501)
    return http.HttpResponse(serializers.serialize('json', item),
            content_type='application/json')

def ean_suggest(request, ean):
    # XXX: Look up in the local database.
    try:
        item = models.Item.objects.get(pk=ean)
    except models.DoesNotExist:
        item = None
        pass

    if item == None:
        # Look up code in EAN database.
        r = json.loads(urllib.urlopen('http://api.upcdatabase.org/json/{}/{}' \
                .format( EAN_APIKEY, ean)).read())

        info = {
            'ean':         r['number'],
            'description': r['description'],
            'ingredient':  r['itemname'],
            'size':        0
        }

    return http.HttpResponse(json.dumps(info),
            content_type='application/json')
