from django.shortcuts import render, redirect
from django.views import View

from honey.forms import HoneyOfferForm, HoneyTasteForm, HoneyVariantForm, HoneyTypeForm, HoneyOfferUpdateForm
from honey.models import HoneyTaste, HoneyType, HoneyVariant, HoneyOffer


class HoneysView(View):
    def get(self, request):
        return render(request, 'honey.html')



class AddHoneyTasteView(View):
    def get(self, request):
        form = HoneyTasteForm()
        return render(request, 'honey_edit_form.html', {'form': form})

    def post(self, request):
        form = HoneyTasteForm(request.POST)
        if form.is_valid():
            taste = form.cleaned_data['taste']
            if HoneyTaste.objects.filter(taste=taste).exists():
                return render(request, 'honey_edit_form.html', {
                    'form': form,
                    'message': 'Taste already exists !'
                })
            form.save()
            return render(request, 'honey_edit_form.html', {'form': form})

class AddHoneyTypeView(View):
    def get(self, request):
        form = HoneyTypeForm()
        return render(request, 'honey_edit_form.html', {'form': form})

    def post(self, request):
        form = HoneyTypeForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data['type']
            if HoneyType.objects.filter(type=type).exists():
                return render(request, 'honey_edit_form.html', {
                    'form': form,
                    'message': 'Type already exists !'
                })
            form.save()
            return render(request, 'honey_edit_form.html', {'form': form})


class AddHoneyVariantView(View):
    def get(self, request):
        form = HoneyVariantForm()
        return render(request, 'honey_edit_form.html', {'form': form})

    def post(self, request):
        form = HoneyVariantForm(request.POST)
        if form.is_valid():
            variant = form.cleaned_data['variant']
            if HoneyVariant.objects.filter(variant=variant).exists():
                return render(request, 'honey_edit_form.html', {
                    'form': form,
                    'message': 'Variant already exists !'
                })
            form.save()
            return render(request, 'honey_edit_form.html', {'form': form})


class AddHoneyOfferView(View):

    def get(self, request):
        form = HoneyOfferForm()
        return render(request, 'honey_offer_form.html', {'form': form})

    def post(self, request):
        form = HoneyOfferForm(request.POST)

        if form.is_valid():
            taste = form.cleaned_data['taste']
            type = form.cleaned_data['type']
            variant = form.cleaned_data['variant']
            honey = HoneyOffer.objects.filter(taste=taste, type=type, variant=variant).first()
            if honey:
                return render(request, 'honey_offer_form.html', {
                    'form': form,
                    'honey': honey,
                    'message': 'Offer already exists !'
                })
            honey = form.save()
            return render(request, 'honey_offer_form.html', {
                'form': form,
                'honey': honey
                })


class HoneyListView(View):
    def get(self, request):
        honeys = HoneyOffer.objects.all().order_by('taste')
        return render(request, 'honey_list.html', {
            'honeys': honeys,
        })



class UpdateHoneyOfferView(View):

    def get(self, request, pk):
        honey = HoneyOffer.objects.get(pk=pk)
        form = HoneyOfferUpdateForm(instance=honey)
        return render(request, 'update_offer_form.html', {
            'form': form,
            'honey': honey
        })

    def post(self, request, pk):
        honey = HoneyOffer.objects.get(pk=pk)
        form = HoneyOfferUpdateForm(request.POST, instance=honey)
        if form.is_valid():
            form.save()
            return render(request, 'update_offer_form.html', {
                'form': form,
                'honey': honey,
                'message': 'Honey updated successfully!'
            })


class DeleteHoneyOfferView(View):
    def get(self, request, pk):
        honey = HoneyOffer.objects.get(pk=pk)
        form = HoneyOfferUpdateForm(instance=honey)
        return render(request, 'delete_form.html', {
            'honey': honey,
            'form': form
        })

    def post(self, request, pk):
        honey = HoneyOffer.objects.get(pk=pk)
        honey.delete()
        return redirect('honey_list')















