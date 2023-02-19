from import_export import resources
from .models import publications

class PublicationResource(resources.ModelResource):
    class meta:
        model = publications
        exclude = ('id')
        skipped_unchanged = True
        report_skipped = True
        import_id_fields = ('title', 'author', 'abstract', 'url', 'pdf', 'source', 'status', 'year')