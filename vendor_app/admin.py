from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Vendor, OpeningHour

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ("user", 'vendor_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'vendor_name')
    list_agitable = ('is_approved',)
admin.site.register(Vendor, VendorAdmin)






class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'day', 'from_hour', 'to_hour')


admin.site.register(OpeningHour, OpeningHourAdmin)