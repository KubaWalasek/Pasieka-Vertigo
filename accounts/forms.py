from django import forms
from django.contrib.auth.models import User

######################################################################################################

class RegisterUserForm(forms.ModelForm):
    password_1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    email = forms.EmailField(required=False)

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
