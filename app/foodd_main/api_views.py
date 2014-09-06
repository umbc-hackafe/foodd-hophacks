from django import http
import foodd_main.models as models

def EANAdd(request):
    # Get and normalize the EAN from the post request.
    ean = models.Item.to_ean(request.POST.get('ean'))

    # Create a response dictionary so whatever calls this can provide
    # more information if necessary.
    jresponse = {'ean': ean}

    try:
        models.Item.ensure_present(ean)
    except models.Item.NeedsIngredient:
        jresponse['needs'] = 'ingredient'
    except models.Item.NeedsData:
        jresponse['needs'] = 'data'

    # XXX: We should attach a Location header here, pointing to the new
    # Item.
    return http.HttpResponse(json.dumps(jresponse), status=201)
