from django.conf import urls
from django.contrib import admin

admin.autodiscover()

urlpatterns = urls.patterns(
    "",
    urls.url(r"^admin/", urls.include(admin.site.urls)),
    urls.url(r"^login/", "django.contrib.auth.views.login", {
        "template_name": "foodd_main/login.html"
    }, name="login"),
    urls.url(r"^logout$", "django.contrib.auth.views.logout", {
        "next_page": "/",
    }, name="logout"),
    urls.url(r"", urls.include("foodd_main.urls"))
)
