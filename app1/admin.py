from django.contrib import admin
from .models import Contact, OrderUpdate, authenticator, Claimed
# Register your models here.

admin.site.register(Contact)
admin.site.register(OrderUpdate)
admin.site.register(authenticator)
admin.site.register(Claimed)
