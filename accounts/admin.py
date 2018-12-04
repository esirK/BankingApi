from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomerBankAccount

User = get_user_model()

admin.site.register(User, UserAdmin)
admin.site.register(CustomerBankAccount)
