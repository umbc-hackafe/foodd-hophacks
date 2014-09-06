from django import http
from django import shortcuts
import json
import os
from urllib import urlopen

hosted_jquery = '<script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>'

UPC_APIKEY = os.getenv('FOODD_UPCDATABASE_KEY')

def home(request):
    return shortcuts.render(request, "foodd_main/base.html")

def upc_info(request, upc):
    # XXX: Look up in the local database.

    # Look up code in UPC database.
    r = urlopen('http://api.upcdatabase.org/json/{}/{}'.format(
        UPC_APIKEY, upc))

    return http.HttpResponse(r, content_type='application/json')
