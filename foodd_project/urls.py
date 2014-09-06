from django.conf import urls

urlpatterns = urls.patterns(
  '',
  urls.url(r'^$', 'foodd_main.views.home'),
)
