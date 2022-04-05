from django.contrib import admin
from .models import User_Account

# Register your models here.

class UserAccount_Admin(admin.ModelAdmin):
    list_display=["user", "first_name", "middle_name", "last_name", "contact_number", "email_address", "profile_pic"]

admin.site.register(User_Account, UserAccount_Admin)