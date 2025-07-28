from django import forms
from django.contrib.auth.models import User

######################################################################################################

class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password_1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password_2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput, required=True)
    email = forms.EmailField(required=True, error_messages={'required': 'Email is required'})
    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)
    post_code = forms.CharField(max_length=10, required=False)
    city = forms.CharField(max_length=30, required=False)
    street = forms.CharField(max_length=30, required=False)
    street_number = forms.CharField(max_length=10, required=False)
    door_number = forms.CharField(max_length=10, required=False)
    phone_number = forms.CharField(max_length=15, required=False)


    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get('password_1')
        password_2 = cleaned_data.get('password_2')

        if password_1 != password_2:
            raise forms.ValidationError('Passwords do not match')

    class Meta:
        model = User
        fields = ['username', 'email']

######################################################################################################

class LoginUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

############################################################################################################


class UpdateUserForm(forms.ModelForm):
    password_1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password_2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput, required=False)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=20, required=False )
    last_name = forms.CharField(max_length=20,required=False )
    post_code = forms.CharField(max_length=10, required=False )
    city = forms.CharField(max_length=30, required=False)
    street = forms.CharField(max_length=30, required=False)
    street_number = forms.CharField(max_length=10, required=False)
    door_number = forms.CharField(max_length=10, required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True  # tu ustawiamy readonly

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get('password_1')
        password_2 = cleaned_data.get('password_2')

        if password_1 != password_2:
            raise forms.ValidationError('Passwords do not match')

    class Meta:
        model = User
        fields = ['username', 'email']
