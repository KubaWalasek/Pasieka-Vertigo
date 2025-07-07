from django import forms
from .models import HoneyOffer, HoneyTaste, HoneyType, HoneyVariant


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

class HoneyOfferUpdateForm(forms.ModelForm):
    class Meta:
        model = HoneyOffer
        fields = ['price', 'quantity']








