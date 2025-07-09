from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from honey.forms import HoneyOfferForm, HoneyTasteForm, HoneyVariantForm, HoneyTypeForm, HoneyOfferUpdateForm, HoneySearchForm
from honey.models import HoneyTaste, HoneyType, HoneyVariant, HoneyOffer

####################################################################################################################
class HoneysView(View):
    def get(self, request):
        return render(request, 'honey.html')

####################################################################################################################

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

####################################################################################################################

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


####################################################################################################################


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


####################################################################################################################


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
                    'message_1': 'Offer already exists !'
                })
            honey = form.save()
            return render(request, 'honey_offer_form.html', {
                'form': form,
                'honey': honey,
                'message': 'Honey offer created successfully!'
                })
        return render(request, 'honey_offer_form.html', {'form': form})


####################################################################################################################


class HoneyListView(View):
    def get(self, request):
        honeys = HoneyOffer.objects.all().order_by('taste')
        return render(request, 'honey_list.html', {
            'honeys': honeys,
        })



####################################################################################################################


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
        return render(request, 'update_offer_form.html', {
            'form': form,
            'honey': honey
        })



####################################################################################################################


class DeleteHoneyOfferView(View):
    def get(self, request, pk):
        honey = HoneyOffer.objects.get(pk=pk)
        return render(request, 'delete_form.html', {
            'honey': honey,
            'message': 'Be careful, you are going to delete this offer !'
        })

    def post(self, request, pk):
        honey = HoneyOffer.objects.get(pk=pk)
        honey.delete()
        return redirect('honey_list')


####################################################################################################################


class HoneyListView(View):
    def get(self, request):
        form = HoneySearchForm(request.GET)
        honeys = HoneyOffer.objects.all().select_related('taste', 'type', 'variant').order_by('taste__taste')

        if form.is_valid():
            query = form.cleaned_data['query']
            if query:
                query_lower = query.lower()
                honeys = [
                    honey for honey in honeys
                    if any(
                        query_lower in value.lower()
                        for value in [
                            honey.taste.taste,
                            honey.taste.get_taste_display(),
                            honey.type.type,
                            honey.type.get_type_display(),
                            honey.variant.variant,
                            honey.variant.get_variant_display(),
                        ]
                    )
                ]
        return render(request, 'honey_list.html', {
            'honeys': honeys,
            'form': form,
        })


####################################################################################################################











