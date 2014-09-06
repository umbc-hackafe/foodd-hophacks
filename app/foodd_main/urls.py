from django.conf import urls
from django.contrib import admin
import foodd_main.views as views

urlpatterns = urls.patterns(
  "",
  urls.url(r"^$", views.HomeView.as_view(), name="home"),
  urls.url(r"^pantry/(?P<pk>[0-9]+)$", views.PantryView.as_view(), name="pantry"),
  urls.url(r"^ingredient$", views.IngredientsView.as_view(), name="ingredients"),
  urls.url(r"^ingredient/(?P<name>\w+)$", views.IngredientView.as_view(), name="ingredient"),
  urls.url(r"^ean/suggest/(?P<ean>[0-9]{6,13})$", views.ean_suggest,
      name="ean_suggest"),
  urls.url(r"^ean/info/(?P<ean>[0-9]{6,13})$", views.ean_info, name="ean_info")
)
