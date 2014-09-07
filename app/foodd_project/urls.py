from django.conf import urls
from django.contrib import admin
import tastypie.api as api
import foodd_main.api.resources as resources

admin.autodiscover()

v1_api = api.Api(api_name='v1')
v1_api.register(resources.IngredientResource())

urlpatterns = urls.patterns(
    "",
    urls.url(r"^admin/", urls.include(admin.site.urls)),
    urls.url(r"^login/", "django.contrib.auth.views.login", {
        "template_name": "foodd_main/login.html"
    }, name="login"),
    urls.url(r"^logout$", "django.contrib.auth.views.logout", {
        "next_page": "/",
    }, name="logout"),
    urls.url(r"^apy/", urls.include(v1_api.urls)),
    urls.url(r"", urls.include("foodd_main.urls"))
)
