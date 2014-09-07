import tastypie.resources as resources
import foodd_main.models as models


class IngredientResource(resources.ModelResource):
    class Meta:
        queryset = models.Ingredient.objects.all()
        allowed_methods = ['get']
