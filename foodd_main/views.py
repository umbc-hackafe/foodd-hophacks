from django import http
from django.views import generic
from django import shortcuts
from django.core import serializers
import models
import json
import os
import urllib

EAN_APIKEY = os.getenv("FOODD_EANDATABASE_KEY")

class HomeView(generic.TemplateView):
    template_name = "foodd_main/base.html"

def ean_info(request, ean):
    return http.HttpResponse(status=501)
    return http.HttpResponse(serializers.serialize('json', item),
            content_type='application/json')

def ean_suggest(request, ean):
    # XXX: Look up in the local database.

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
