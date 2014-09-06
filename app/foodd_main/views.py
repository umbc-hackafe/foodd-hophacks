from django import http
from django.views import generic
from django import shortcuts
from django.core import serializers
from django.core import exceptions
from django.db.models import Q
import foodd_main.models as models
import logging
import json
import os
import urllib.request
import foodd_project.settings as settings

EAN_APIKEY = os.getenv("FOODD_EANDATABASE_KEY")

class HomeView(generic.TemplateView):
    template_name = "foodd_main/home.html"

class SearchView(generic.ListView):
    template_name = "foodd_main/search.html"
    context_object_name = "recipes"

    def get_queryset(self):
        return models.Recipe.objects.filter(Q(description__contains=self.kwargs['query'])
                                            | Q(name__contains=self.kwargs['query']))

    def get_context_data(self):
        context = super(SearchView, self).get_context_data()
        context['query'] = self.kwargs['query']
        return context

class PantryView(generic.ListView):
    template_name = "foodd_main/pantry.html"
    context_object_name = "pantry_items"

    def get_queryset(self):
        self.pantry = shortcuts.get_object_or_404(
            models.Pantry, pk=self.kwargs["pk"])
        return models.PantryItem.objects.filter(pantry=self.pantry)

    def get_context_data(self):
        context = super(PantryView, self).get_context_data()
        context["pantry"] = self.pantry
        return context

class ItemView(generic.DetailView):
    template_name = "foodd_main/item.html"
    context_object_name = "item"

    def get_queryset(self):
        return models.Item.objects.filter(ean=self.kwargs["pk"])

class IngredientsView(generic.ListView):
    template_name = "foodd_main/ingredients.html"
    context_object_name = "ingredients"
    queryset = models.Ingredient.objects.all()

class IngredientView(generic.DetailView):
    context_object_name = "ingredient"
    template_name = "foodd_main/ingredient.html"

    def get_queryset(self):
        return shortcuts.get_object_or_404(
            models.Ingredient, name__iexact=self.kwargs["name"])

def EANInfo(request, ean):
    return http.HttpResponse(status=501)
    return http.HttpResponse(serializers.serialize('json', item),
            content_type='application/json')

def EANSuggest(request, ean):
    try:
        item = models.Item.objects.get(pk=ean)
    except exceptions.ObjectDoesNotExist:
        logging.info("EAN {} not in database, querying upcdatabase.org"
                .format(ean))
        item = None

    if item != None:
        info = {
            'ean':         item.ean,
            'description': item.description,
            'ingredient':  item.ingredient.name,
            'size':        item.size
        }

    else:
        # Look up code in EAN database.
        # XXX: Do this more efficiently.
        resp = urllib.request.urlopen(
                'http://api.upcdatabase.org/json/{}/{}'.format(
                    settings.EAN_APIKEY, ean))
        r = json.loads(resp.read().decode('utf8'))

        if r["valid"] == "true":
            info = {
                'ean':         r['number'],
                'description': r['description'],
                'ingredient':  r['itemname'],
                'size':        0
            }
        else:
            info = {}

    return http.HttpResponse(json.dumps(info),
            content_type='application/json')
