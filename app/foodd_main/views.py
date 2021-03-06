from django import http
from django.views import generic
from django import shortcuts
from django.core import serializers
from django.core import exceptions
from django.core.urlresolvers import reverse
from django.core import paginator
from django.db.models import Q
from django.contrib.auth import decorators, authenticate, login
import foodd_main.models as models
from foodd_main import forms
import logging
import json
import os
import urllib.request
import foodd_project.settings as settings

EAN_APIKEY = os.getenv("FOODD_EANDATABASE_KEY")

class LoginRequiredMixin(generic.base.View):
    @classmethod
    def as_view(cls, *args, **kwargs):
        return decorators.login_required(super(LoginRequiredMixin, cls).as_view(*args, **kwargs))

class HomeView(generic.TemplateView):
    template_name = "foodd_main/home.html"

class SearchView(generic.ListView):
    template_name = "foodd_main/search.html"
    context_object_name = "recipes"

    def get_queryset(self):
        self.query = self.request.GET.get('q')
        return models.Recipe.objects.filter(
            Q(description__contains=self.query) | Q(name__contains=self.query))

    def get_context_data(self):
        context = super(SearchView, self).get_context_data()
        context["ingredients"] = models.Item.objects.filter(
            Q(name__contains=self.query) | Q(description__contains=self.query) |
            Q(ingredient__name__contains=self.query))
        context["page"] = self.request.GET.get("page")
        context["tab"] = self.request.GET.get("tab")
        context["tab"] = context["tab"] if context["tab"] and context["tab"] in ("ingredients", "recipes") else "recipes"
        context["paginator"] = paginator.Paginator(context[context["tab"]], 20)
        try:
            context["items"] = context["paginator"].page(context["page"])
            context["page"] = int(context["page"])
        except paginator.PageNotAnInteger:
            context["page"] = 1
            context["items"] = context["paginator"].page(1)
        except paginator.EmptyPage:
            context["page"] = context["paginator"].num_pages
            context["items"] = context["paginator"].page(context["paginator"].num_pages)
        context["query"] = self.query
        return context

class PantryView(generic.ListView, LoginRequiredMixin):
    template_name = "foodd_main/pantry.html"
    context_object_name = "pantry_items"

    def get_queryset(self):
        self.pantry = shortcuts.get_object_or_404(
            models.Pantry, pk=self.kwargs["pk"])
        return models.PantryItem.objects.filter(pantry=self.pantry)

    def get_context_data(self):
        context = super(PantryView, self).get_context_data()
        context["pantry"] = self.pantry
        return context

class ItemView(generic.DetailView, LoginRequiredMixin):
    template_name = "foodd_main/item.html"
    context_object_name = "item"

    def get_queryset(self):
        return models.Item.objects.filter(ean=self.kwargs["pk"])

class IngredientsView(generic.ListView):
    template_name = "foodd_main/ingredients.html"
    context_object_name = "ingredients"
    queryset = models.Ingredient.objects.all()

class IngredientView(generic.DetailView):
    context_object_name = "ingredient"
    template_name = "foodd_main/ingredient.html"

    def get_queryset(self):
        return shortcuts.get_object_or_404(
            models.Ingredient, name__iexact=self.kwargs["name"])

def UserCreateView(request):
    # Boolean telling us whether registration was successful or not.
    # Initially False; presume it was a failure until proven otherwise!
    registered = False

    # If HTTP POST, we wish to process form data and create an account.
    if request.method == 'POST':
        # Grab raw form data - making use of both FormModels.
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.FooddUserForm(data=request.POST)

        # Two valid forms?
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data. That one is easy.
            user = user_form.save()

            # Now a user account exists, we hash the password with the set_password() method.
            # Then we can update the account with .save().
            user.set_password(user.password)
            user.save()

            # Now we can sort out the TangleUser instance.
            # We'll be setting values for the instance ourselves, so
            # commit=False prevents Django from saving the instance
            # automatically.

            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the model instance!
            profile.save()
            profile_form.save_m2m()

            # We can say registration was successful.
            registered = True

            return shortcuts.redirect("home")

        # Invalid form(s) - just print errors to the terminal.
        else:
            logging.info("User Errors: %s Profile Errors: %s", user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render the two ModelForms to allow a user
    # to input their data.
    else:
        user_form = forms.UserForm()
        profile_form = forms.FooddUserForm()

    # Render and return!
    return shortcuts.render(
            request, 'foodd_main/user_create.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

class PantryCreateView(generic.edit.CreateView, LoginRequiredMixin):
    template_name = "foodd_main/pantry_create.html"
    form_class = forms.PantryForm

    def form_valid(self, form):
        fuser = models.FooddUser.objects.get(user=self.request.user)
        fuser.save()

        m = models.PantryMembership(user=fuser, pantry=form.save(), permissions='O')
        m.save()

        return super(PantryCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("pantry", args=(self.object.pk,))

def EANInfo(request, ean):
    return http.HttpResponse(status=501)
    return http.HttpResponse(serializers.serialize('json', item),
            content_type='application/json')

def EANSuggest(request, ean):
    try:
        item = models.Item.objects.get(pk=ean)
    except exceptions.ObjectDoesNotExist:
        logging.info("EAN {} not in database, querying upcdatabase.org"
                .format(ean))
        item = None

    if item != None:
        info = {
            'ean':         item.ean,
            'description': item.description,
            'ingredient':  item.ingredient.name,
            'size':        item.size
        }

    else:
        # Look up code in EAN database.
        # XXX: Do this more efficiently.
        resp = urllib.request.urlopen(
                'http://api.upcdatabase.org/json/{}/{}'.format(
                    settings.EAN_APIKEY, ean))
        r = json.loads(resp.read().decode('utf8'))

        if r["valid"] == "true":
            info = {
                'ean':         r['number'],
                'description': r['description'],
                'ingredient':  r['itemname'],
                'size':        0
            }
        else:
            info = {}

    return http.HttpResponse(json.dumps(info),
            content_type='application/json')
