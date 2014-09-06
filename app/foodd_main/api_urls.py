from django.conf import urls
import foodd_main.api_views as api

urlpatterns = urls.patterns(
  "",
  urls.url(r"^ean/add$", api.EANAdd, name="EANAdd"),
  urls.url(r"^item/complete$", api.ItemComplete, name="ItemComplete")
  urls.url(r"^pantry/item/get$", api.PantryItemGet, name="PantryItemGet")
