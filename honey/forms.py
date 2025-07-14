from django import forms
from .models import HoneyOffer, HoneyTaste, HoneyType, HoneyVariant, BeeProduct
from django.core.validators import MinValueValidator


class HoneyOfferForm(forms.ModelForm):
    class Meta:
        model = HoneyOffer
        fields = '__all__'

class HoneyTasteForm(forms.ModelForm):
    class Meta:
        model = HoneyTaste
        fields = '__all__'

class HoneyTypeForm(forms.ModelForm):
    class Meta:
        model = HoneyType
        fields = '__all__'

class HoneyVariantForm(forms.ModelForm):
    class Meta:
        model = HoneyVariant
        fields = '__all__'

class BeeProductForm(forms.ModelForm):
    class Meta:
        model = BeeProduct
        fields = '__all__'

class HoneyOfferUpdateForm(forms.ModelForm):
    class Meta:
        model = HoneyOffer
        fields = ['price', 'quantity']

class BeeProductUpdateForm(forms.ModelForm):
    class Meta:
        model = BeeProduct
        fields = ['price', 'quantity']


class HoneySearchForm(forms.Form):
    query = forms.CharField(
        max_length=20,
        label='',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wpisz czego szukasz...'})
    )






