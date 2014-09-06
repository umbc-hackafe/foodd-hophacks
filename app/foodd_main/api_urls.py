from django.conf import urls
import foodd_main.api_views as api

urlpatterns = urls.patterns(
  "",
  urls.url(r"^ean/add$", api.EANAdd, name="add EAN"),
  urls.url(r"^item/complete$", api.ItemComplete, name="complete item")
)
