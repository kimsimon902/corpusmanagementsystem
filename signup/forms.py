from .models import publications
from django import forms
import re


class publicationForm(forms.Form):
    class meta:
        model = publications
        fields = '__all__'