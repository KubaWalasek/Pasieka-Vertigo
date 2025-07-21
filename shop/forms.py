from django import forms
from honey.models import BeeProduct, HoneyOffer


class AddToCartHoneyForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = HoneyOffer
        fields = ['quantity']

    def __init__(self, *args, available_quantity=1, **kwargs ):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].min_value = 1
        self.fields['quantity'].max_value = available_quantity
        self.fields['quantity'].widget.attrs['min'] = 1
        self.fields['quantity'].widget.attrs['max'] = available_quantity


class AddToCartBeeProductForm(forms.ModelForm):
    class Meta:
        model = BeeProduct
        fields = ['quantity']

    def __init__(self, *args, available_quantity=1, **kwargs ):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].min_value = 1
        self.fields['quantity'].max_value = available_quantity
        self.fields['quantity'].widget.attrs['min'] = 1
        self.fields['quantity'].widget.attrs['max'] = available_quantity



