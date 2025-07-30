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


class OrderDataForm(forms.Form):
    first_name = forms.CharField(label="Imię", max_length=20, required=True)
    last_name = forms.CharField(label="Nazwisko", max_length=20, required=True)
    email = forms.EmailField(label="E-mail", required=True)
    post_code = forms.CharField(label="Kod pocztowy", max_length=10, required=True)
    city = forms.CharField(label="Miasto", max_length=30, required=True)
    street = forms.CharField(label="Ulica", max_length=30, required=True)
    street_number = forms.CharField(label="Nr domu", max_length=10, required=True)
    door_number = forms.CharField(label="Nr mieszkania", max_length=10, required=False)
    phone_number = forms.CharField(label="Telefon", max_length=15, required=True)



