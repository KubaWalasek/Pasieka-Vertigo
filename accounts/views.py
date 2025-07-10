from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import RegisterUserForm, LoginUserForm


class RegisterView(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, 'account_form.html', {
            'form': form,
        })

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password_1'])
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        return render(request, 'account_form.html', {
            'form': form,
        })

class LoginView(View):
    def get(self, request):
        form = LoginUserForm()
        return render(request, 'account_form.html', {
            'form': form,
        })

    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                return render(request, 'account_form.html', {
                    'form': form,
                    'message': 'Invalid username or password !'})
        return render(request, 'account_form.html', {
            'form': form,
        })

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class UserAccountView(LoginRequiredMixin, View):
    def get(self, request):
        form = RegisterUserForm(instance=request.user)
        form.fields['username'].disabled = True
        form.fields['password_1'].required = False
        form.fields['password_2'].required = False
        form.fields['email'].required = False
        return render(request, 'account_form.html', {
            'form': form,
            'message': 'You can edit your account here !',
            'url': 'user_account'
        })

    def post(self, request):
        form = RegisterUserForm(request.POST, instance=request.user)
        form.fields['username'].disabled = True
        form.fields['password_1'].required = False
        form.fields['password_2'].required = False
        form.fields['email'].required = False
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password_1']:
                user.set_password(form.cleaned_data['password_1'])
            user.save()
            messages.success(request, 'Account updated successfully!')
            return redirect('user_account')
        return render(request, 'account_form.html', {
            'form': form,
            'message': 'You can edit your account here !'
        })

