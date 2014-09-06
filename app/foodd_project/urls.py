from django.conf import urls
from django.contrib import admin

admin.autodiscover()

urlpatterns = urls.patterns(
    "",
    urls.url(r"^admin/", urls.include(admin.site.urls)),
    urls.url(r"", urls.include("foodd_main.urls"))
)
