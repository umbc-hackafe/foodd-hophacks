from django import http
from django.core import exceptions
import foodd_main.models as models
import json

def EANAdd(request):
    # Get and normalize the EAN from the post request.
    try:
        ean = models.Item.to_ean(request.POST.get('ean'))
    except models.Item.InvalidEAN:
        return http.HttpResponseBadRequest()

    # Create a response dictionary so whatever calls this can provide
    # more information if necessary.
    jresponse = {'ean': ean}

    # At this point, check whether the Item exists already. If so, don't
    # do anything.
    try:
        item = models.Item.objects.get(pk=ean)
        jresponse['new'] = False
        if item.description == None or item.size == None:
            raise models.Items.NeedsIngredient("missing item data")
        elif item.ingredient == None:
            raise models.Items.NeedsData("missing item data")

        return http.HttpResponse(json.dumps(jresponse))
    except exceptions.ObjectDoesNotExist:
        jresponse['new'] = True

    try:
        models.Item.ensure_present(ean)
    except models.Item.NeedsIngredient:
        jresponse['needs'] = 'ingredient'
    except models.Item.NeedsData:
        jresponse['needs'] = 'data'

    # XXX: We should attach a Location header here, pointing to the new
    # Item.
    return http.HttpResponse(json.dumps(jresponse), status=201)

def ItemComplete(request):
    # Get the query string from the request.
    query = request.GET.get('q')
    suggestions = []

    # If the query was given, populate the suggestions.
    if query:
        matchset = models.Item.objects.filter(name__icontains = query)
        suggestions = [{'ean': item.ean, 'name': item.name} for item in
                matchset]

    return http.HttpResponse(json.dumps(suggestions))
