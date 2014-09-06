from django.conf import urls

urlpatterns = urls.patterns(
  "",
  urls.url(r"", urls.include("foodd_main.urls"))
)
