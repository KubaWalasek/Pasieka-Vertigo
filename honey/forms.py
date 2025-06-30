from django import forms
from .models import Honey

class HoneyForm(forms.ModelForm):
    class Meta:
        model = Honey
        fields = ('type', 'size', 'price', 'quantity')

class HoneyUpdateForm(forms.ModelForm):
    class Meta:
        model = Honey
        fields = ( 'price', 'quantity')


