from django import http
from django.core import exceptions
from django.core import serializers
from foodd_main import models
import logging
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
        if request.POST.get('ean') is None:
            logging.error("Key 'ean' not found in request.POST")
        else:
            loggign.error("EAN %s was considered invalid.", request.POST.get('ean'))
        return http.HttpResponseBadRequest()

    count = request.POST.get('count')
    if not count or int(count) <= 0:
        if request.POST.get('count') is None:
            logging.error("Key 'count' missing in request.POST")
        else:
            logging.error("Count value %s <= 0", request.POST.get('count'))
        return http.HttpResponseBadRequest()

    try:
        pantry = models.Pantry.objects.get(pk=request.POST.get('pk'))
    except exceptions.ObjectDoesNotExist:
        if request.POST.get('pk') is None:
            logging.error("Key 'pk' not found in request.POST")
        else:
            logging.error("Pantry with pk=%s not found", request.POST.get('pk'))
        return http.HttpResponseBadRequest()

    # At this point, check whether the Item exists already. If so, don't
    # do anything.
    item = models.Item.ensure_present(ean=ean)

    if not item:
        logging.error("Unable to ensure the presence of an item with EAN %s", ean)
        return http.HttpResponseBadRequest()

    pantry_item, created = models.PantryItem.objects.get_or_create(
        pantry=pantry, item=item, defaults={'remaining': count})

    if not created:
        pantry_item.remaining += int(count)

    pantry_item.save()

    inner_item = serializers.serialize('json', [pantry_item.item])
    logging.info(inner_item)
    return http.HttpResponse(serializers.serialize('json', [pantry_item]), content_type='application/json')


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
