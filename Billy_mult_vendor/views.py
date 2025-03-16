
from django.shortcuts import render
from vendor_app.models import Vendor

def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True )[:8]#this will limit the restaurant by 8 if it more than that in in the homepage

    context = {
        'vendors': vendors,
    }
    return render(request,'home.html', context)