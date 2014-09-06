from django import http
from django.views import generic
from django import shortcuts
from django.core import serializers
import models
import json
import os
import urllib

UPC_APIKEY = os.getenv("FOODD_UPCDATABASE_KEY")

class HomeView(generic.TemplateView):
    template_name = "foodd_main/base.html"

def upc_info(request, upc):
    return http.HttpResponse(status=501)
    return http.HttpResponse(serializers.serialize('json', item),
            content_type='application/json')

def upc_suggest(request, upc):
    # XXX: Look up in the local database.

    # Look up code in UPC database.
    r = json.loads(urllib.urlopen('http://api.upcdatabase.org/json/{}/{}' \
            .format( UPC_APIKEY, upc)).read())

    info = {
        'upc':         r['number'],
        'description': r['description'],
        'ingredient':  r['itemname'],
        'size':        0
    }

    return http.HttpResponse(json.dumps(info),
            content_type='application/json')
