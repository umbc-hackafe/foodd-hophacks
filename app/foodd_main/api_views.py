from django import http
from django.core import exceptions
import foodd_main.models as models

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
        models.Item.objects.get(pk=ean)
        jresponse['new'] = False
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
