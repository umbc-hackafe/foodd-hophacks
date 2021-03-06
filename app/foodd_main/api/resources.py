import tastypie.resources as resources
import foodd_main.models as models
import tastypie.authorization as auth

class IngredientResource(resources.ModelResource):
    class Meta:
        queryset = models.Ingredient.objects.all()
        resource_name = 'ingredient'
        allowed_methods = ['get']
        filtering = {
            'id': 'exact',
            'properties': resources.ALL,
            'unit': 'exact',
            'provides': resources.ALL,
            'name': resources.ALL_WITH_RELATIONS
        }

class PropertyResource(resources.ModelResource):
    class Meta:
        queryset = models.Property.objects.all()
        resource_name = 'property'

class ItemResource(resources.ModelResource):
    class Meta:
        queryset = models.Item.objects.all()
        resource_name = 'item'

class PantryItemResource(resources.ModelResource):
    class Meta:
        queryset = models.PantryItem.objects.all()
        resource_name = 'pantry-item'
        allowed_methods = ['get', 'delete', 'put', 'patch']
        authorization = auth.DjangoAuthorization()
