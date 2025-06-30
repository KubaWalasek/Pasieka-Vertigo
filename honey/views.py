from django.shortcuts import render, redirect
from django.views import View

from honey.forms import HoneyForm, HoneyUpdateForm
from honey.models import Honey



class AddHoneyView(View):

    def get(self, request):
        form = HoneyForm()
        honeys = Honey.objects.all().order_by('type')
        return render(request, 'add_honey.html', {'form': form, 'honeys': honeys})

    def post(self, request):
        form = HoneyForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data['type']
            size = form.cleaned_data['size']

            if Honey.objects.filter(type=type, size=size).exists():
               return render(request, 'add_honey.html', {
                   'form': form,
                   'honeys': Honey.objects.all().order_by('type'),
                   'message': 'Honey already exists !'
               })
            else:
                form.save()
            return redirect('add_honey')
        honeys = Honey.objects.all().order_by('type')
        return render(request, 'add_honey.html', {'form': form, 'honeys': honeys})

class UpdateHoneyView(View):

    def get(self, request, pk):
        honey = Honey.objects.get(pk=pk)
        form = HoneyUpdateForm(instance=honey)
        return render(request, 'update_honey.html', {'form': form, 'honey': honey})

    def post(self, request, pk):
        honey = Honey.objects.get(pk=pk)
        form = HoneyUpdateForm(request.POST, instance=honey)
        if form.is_valid():
            form.save()
            return render(request, 'update_honey.html', {
                'form': form,
                'honey': honey,
                'message': 'Honey updated successfully!'})


class DeleteHoneyView(View):
    def get(self, request, pk):
        honey = Honey.objects.get(pk=pk)
        return render(request, 'delete_honey.html', {'honey': honey})

    def post(self, request, pk):
        honey = Honey.objects.get(pk=pk)
        honey.delete()
        return redirect('add_honey')















