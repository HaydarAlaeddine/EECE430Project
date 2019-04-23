from django import forms
from django.contrib.auth.models import User

class RequestDocumentForm(forms.Form):
    description = forms.CharField()
    class Meta:
        fields = ['description']