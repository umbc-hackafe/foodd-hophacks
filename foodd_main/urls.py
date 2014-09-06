from django.conf import urls
import views

urlpatterns = urls.patterns(
  "",
  urls.url(r"^$", views.HomeView.as_view(), name="home"),
  urls.url(r"^ean/suggest/(?P<ean>[0-9]{6,13})$", views.ean_suggest,
      name="ean_suggest"),
  urls.url(r"^ean/info/(?P<ean>[0-9]{6,13})$", views.ean_info, name="ean_info")
)
