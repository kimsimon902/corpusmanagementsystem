from import_export import resources
from .models import publications

class publicationResource(resources.ModelResource):
    class meta: 
        model = publications