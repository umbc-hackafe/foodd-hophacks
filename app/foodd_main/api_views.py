from django import http
from django.core import exceptions
from django.core import serializers
from foodd_main import models
import json

def ItemAutocomplete(request):
    # Get the query string from the request.
    query = request.GET.get('q')
    suggestions = []

    # If the query was given, populate the suggestions.
    if query:
        matchset = models.Item.objects.filter(name__icontains = query)
        suggestions = [{'ean': item.ean, 'name': item.name} for item in
                matchset]

    return http.HttpResponse(json.dumps(suggestions))

def PantryItemAdd(request):
    # Get and normalize the EAN from the post request.
    try:
        ean = models.Item.to_ean(request.POST.get('ean'))
    except models.Item.InvalidEAN:
        return http.HttpResponseBadRequest()

    count = request.POST.get('count')
    if not count or count < 0:
        return http.HttpResponseBadRequest()

    try:
        pantry = models.Pantry.objects.get(pk=request.POST.get('pk'))
    except exceptions.ObjectDoesNotExist:
        return http.HttpResponseBadRequest()

    # At this point, check whether the Item exists already. If so, don't
    # do anything.
    item = models.Item.ensure_present(ean=ean)

    if not item:
        return http.HttpResponseBadRequest()

    pantry_item, created = models.PantryItem.objects.get_or_create(
        pantry=pantry, item=item, defaults={'remaining': count})

    if not created:
        pantry_item.remaining += count

    pantry_item.save()

    return http.HttpResponse(serializers.serialize('json', pantry_item), content_type='application/json')


def PantryItemGet(request):
    # Get the Pantry ID from the request.
    pantry = request.GET.get('pantry')

    # Get the EAN from the request.
    try:
        ean = models.Item.to_ean(request.GET.get('ean'))
    except models.Item.InvalidEAN:
        return http.HttpResponseBadRequest()

    pantryitem = models.PantryItem.objects.get(pantry__pk = pantry,
            item__ean = ean)

    return http.HttpResponse(serializers.serialize('json', pantryitem), content_type='application/json')
