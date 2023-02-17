from django import forms
from .models import publications

class publicationsForm(forms.Form):
    class meta:
        model = publications
        fields = '__all__'