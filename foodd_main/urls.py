from django.conf import urls
import views

urlpatterns = urls.patterns(
  '',
  urls.url(r'^$', views.home),
)