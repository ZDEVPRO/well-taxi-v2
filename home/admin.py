from django.contrib import admin
from home.models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ['qayerdan', 'qayerga', 'client_phone', 'client_name', 'person_count', 'price', 'status']
    readonly_fields = ['create_time', 'create_date']


class TempAdmin(admin.ModelAdmin):
    list_display = ['qayerdan', 'qayerga', 'client_phone', 'client_name', 'person_count', 'price', 'status']
    readonly_fields = ['create_time', 'create_date']


class ArchOrderAdmin(admin.ModelAdmin):
    list_display = ['qayerdan', 'qayerga', 'client_phone', 'client_name', 'person_count', 'price', 'status']
    readonly_fields = ['customer', 'driver', 'qayerdan', 'qayerga', 'client_phone', 'client_name', 'person_count', 'price', 'status', 'create_time', 'create_date']



admin.site.register(TempOrder, TempAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ArchiveOrder, ArchOrderAdmin)
admin.site.register(User)
admin.site.register(Price)
admin.site.register(Region)
admin.site.register(Filter)
