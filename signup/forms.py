from .models import publications
from django import forms

class PublicationForm(forms.Form):
    class meta:
        model = publications
        fields = '__all__'