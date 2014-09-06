from django.conf import urls
import foodd_main.api_views as api

urlpatterns = urls.patterns(
  "",
  urls.url(r"^item/autocomplete$", api.ItemAutocomplete, name="ItemAutocomplete"),
  urls.url(r"^pantry/item/add$", api.PantryItemAdd, name="PantryItemAdd"),
  urls.url(r"^pantry/item/get$", api.PantryItemGet, name="PantryItemGet"))
