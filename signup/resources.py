from import_export import resources
from .models import publications

class PublicationResource(resources.ModelResource):
    class meta:
        model = publications