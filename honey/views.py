from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from honey.forms import HoneyOfferForm, HoneyTasteForm, HoneyVariantForm, HoneyTypeForm, HoneyOfferUpdateForm, \
    HoneySearchForm, BeeProductForm, BeeProductUpdateForm
from honey.models import HoneyTaste, HoneyType, HoneyVariant, HoneyOffer, BeeProduct
from shop.models import CartItem


####################################################################################################################
class HoneysView(View):
    def get(self, request):

        return render(request, 'honey.html')

####################################################################################################################

class AddHoneyTasteView(PermissionRequiredMixin, View):
    permission_required = 'honey.add_honeytaste'

    def handle_no_permission(self):
        # Wyświetl widok z własnym komunikatem lub przekieruj
        return render(self.request,'honey_edit_form.html',{'message': 'You have no permissions.'})

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

class AddHoneyTypeView(PermissionRequiredMixin, View):
    permission_required = 'honey.add_honeytype'

    def handle_no_permission(self):
        # Wyświetl widok z własnym komunikatem lub przekieruj
        return render(self.request,'honey_edit_form.html',{'message': 'You have no permissions.'})

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


class AddHoneyVariantView(PermissionRequiredMixin, View):
    permission_required = 'honey.add_honeyvariant'

    def handle_no_permission(self):
        # Wyświetl widok z własnym komunikatem lub przekieruj
        return render(self.request,'honey_edit_form.html',{'message': 'You have no permissions.'})

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

class AddBeeProductView(PermissionRequiredMixin, View):
    permission_required = 'honey.add_beeproduct'

    def handle_no_permission(self):
        # Wyświetl widok z własnym komunikatem lub przekieruj
        return render(self.request,'honey_edit_form.html',{'message': 'You have no permissions.'})

    def get(self, request):
        form = BeeProductForm()
        return render(request, 'honey_edit_form.html', {'form': form})

    def post(self, request):
        form = BeeProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if BeeProduct.objects.filter(name=name).exists():
                return render(request, 'honey_edit_form.html', {
                    'form': form,
                    'message': 'Product already exists !'
                })
            form.save()
            return render(request, 'honey_edit_form.html', {'form': form})


class AddHoneyOfferView(PermissionRequiredMixin, View):
    permission_required = 'honey.add_honeyoffer'

    def handle_no_permission(self):
        # Wyświetl widok z własnym komunikatem lub przekieruj
        return render(self.request,'honey_edit_form.html',{'message': 'You have no permissions.'})


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




class UpdateHoneyOfferView(PermissionRequiredMixin, View):
    permission_required = 'honey.change_honeyoffer'

    def handle_no_permission(self):
        # Wyświetl widok z własnym komunikatem lub przekieruj
        return render(self.request,'honey_edit_form.html',{'message': 'You have no permissions.'})


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


class DeleteHoneyOfferView(PermissionRequiredMixin, View):
    permission_required = 'honey.delete_honeyoffer'

    def handle_no_permission(self):
        # Wyświetl widok z własnym komunikatem lub przekieruj
        return render(self.request,'honey_edit_form.html',{'message': 'You have no permissions.'})


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


class HoneyListAndSearchView(View):
    def get(self, request):
        form = HoneySearchForm(request.GET)
        honeys = HoneyOffer.objects.all().select_related('taste', 'type', 'variant').order_by('taste__taste') #polega na **optymalizacji liczby zapytań do bazy danych** i wydajności odczytu powiązanych obiektów.
        products = BeeProduct.objects.all()
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
                products = products.filter(name__icontains=query)



        return render(request, 'honey_list.html', {
            'honeys': honeys,
            'products': products,
            'form': form,
        })


####################################################################################################################


class UpdateBeeProductView(PermissionRequiredMixin, View):
    permission_required = 'honey.change_beeproduct'

    def handle_no_permission(self):
        # Wyświetl widok z własnym komunikatem lub przekieruj
        return render(self.request,'honey_edit_form.html',{'message': 'You have no permissions.'})


    def get(self, request, pk):
        product = BeeProduct.objects.get(pk=pk)
        form = BeeProductUpdateForm(instance=product)
        return render(request, 'update_product.html', {
            'form': form,
            'product': product
        })

    def post(self, request, pk):
        product = BeeProduct.objects.get(pk=pk)
        form = BeeProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return render(request, 'update_product.html', {
                'form': form,
                'product': product,
                'message': 'Product updated successfully!'
            })
        return render(request, 'update_product.html', {
            'form': form,
            'product': product
        })



####################################################################################################################


class DeleteBeeProductView(PermissionRequiredMixin, View):
    permission_required = 'honey.delete_beeproduct'

    def handle_no_permission(self):
        # Wyświetl widok z własnym komunikatem lub przekieruj
        return render(self.request,'honey_edit_form.html',{'message': 'You have no permissions.'})

    def get(self, request, pk):
        product = BeeProduct.objects.get(pk=pk)
        return render(request, 'delete_product.html', {
            'product': product,
            'message': 'Be careful, you are going to delete this product !'
        })

    def post(self, request, pk):
        product = BeeProduct.objects.get(pk=pk)
        product.delete()
        return redirect('honey_list')








