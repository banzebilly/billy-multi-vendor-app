
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount, UserProfile
# Define a custom UserAdmin class
class UserAccountAdmin(UserAdmin):
    # Fields to be used in displaying the User model.
    list_display = ('email', 'username', 'first_name', 'last_name','role', 'is_staff')
    
    # Fields that can be searched in the admin interface
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    # Filters available in the admin interface
    list_filter = ('is_staff', 'is_admin', 'is_active', 'role')
    
    # The fieldsets that are used to organize fields in the admin interface
    fieldsets = ()
    
    # Specify fields to be read-only
    readonly_fields = ('last_login', 'date_joined', 'modified_date')
    
    # For handling horizontal filters, if any
    filter_horizontal = ('groups', 'user_permissions')

# Register the custom UserAdmin with the User model
admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(UserProfile)
