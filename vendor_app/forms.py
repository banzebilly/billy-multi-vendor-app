
from django import forms
from .models import Vendor, OpeningHour


class VendorForm(forms.ModelForm):
    
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']

        #we need to connect these two forms USer form and vendor  

class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']        