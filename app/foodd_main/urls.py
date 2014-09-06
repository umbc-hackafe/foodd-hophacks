from django.conf import urls
import views

urlpatterns = urls.patterns(
  "",
  urls.url(r"^$", views.HomeView.as_view(), name="home"),
  urls.url(r"^ingredient$", views.IngredientsView.as_view(), name="ingredients"),
  urls.url(r"^ingredient/(?P<name>\w+)$", views.IngredientView.as_view(), name="ingredient"),
  urls.url(r"^ean/suggest/(?P<ean>[0-9]{6,13})$", views.ean_suggest,
      name="ean_suggest"),
  urls.url(r"^ean/info/(?P<ean>[0-9]{6,13})$", views.ean_info, name="ean_info")
)
