from django import http
from django.views import generic
import json
import os
import urllib

UPC_APIKEY = os.getenv("FOODD_UPCDATABASE_KEY")

class HomeView(generic.TemplateView):
    template_name = "foodd_main/base.html"

def upc_info(request, upc):
    # XXX: Look up in the local database.

    # Look up code in UPC database.
    r = urllib.urlopen("http://api.upcdatabase.org/json/{}/{}".format(
        UPC_APIKEY, upc))

    return http.HttpResponse(r, content_type="application/json")
