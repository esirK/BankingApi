from django.contrib import admin
from django.contrib.auth import get_user_model

from accounts.models import CustomerBankAccount

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_activated', 'is_superuser')
    list_filter = ('is_staff', 'is_activated')


admin.site.register(User, UserAdmin)
admin.site.register(CustomerBankAccount)
