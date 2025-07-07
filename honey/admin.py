from django.contrib import admin
from .models import HoneyTaste, HoneyType, HoneyVariant, HoneyOffer

admin.site.register(HoneyTaste)
admin.site.register(HoneyType)
admin.site.register(HoneyVariant)
admin.site.register(HoneyOffer)