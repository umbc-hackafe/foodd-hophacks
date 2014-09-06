from django.conf import urls
import foodd_main.views as views

urlpatterns = urls.patterns(
  "",
  urls.url(r"^$", views.HomeView.as_view(), name="home"),
  urls.url(r"^pantry/(?P<pk>[0-9]+)$", views.PantryView.as_view(), name="pantry"),
  urls.url(r"^item/(?P<ean>[0-9]{13})$", views.ItemView.as_view(), name="item"),
  urls.url(r"^ingredient$", views.IngredientsView.as_view(), name="ingredients"),
  urls.url(r"^ingredient/(?P<name>\w+)$", views.IngredientView.as_view(), name="ingredient"),
  urls.url(r"^ean/suggest/(?P<ean>[0-9]{6,13})$", views.EANSuggest,
      name="ean suggestion"),
  urls.url(r"^ean/info/(?P<ean>[0-9]{6,13})$", views.EANInfo, name="ean info")
)
