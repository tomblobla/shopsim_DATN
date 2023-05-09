from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer

# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'phone_number',
        'first_name',
        'last_name',
        'last_login',
        'is_active',
    )

    list_display_links = ('email', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Customer, AccountAdmin)
