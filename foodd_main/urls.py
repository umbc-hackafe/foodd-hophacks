from django.conf import urls
import views

urlpatterns = urls.patterns(
  '',
  urls.url(r'^$', views.home),
  urls.url(r'^upc/info/(?P<upc>[0-9]{6,13})$', views.upc_info)
)
