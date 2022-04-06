from django.contrib import admin
from .models import User_Account, Trips

# Register your models here.

class UserAccount_Admin(admin.ModelAdmin):
    list_display=["user", "first_name", "middle_name", "last_name", "contact_number", "email_address", "profile_pic"]
class Trips_Admin(admin.ModelAdmin):
    list_display=["ref_num", "start_time", "create_date"]

admin.site.register(User_Account, UserAccount_Admin)
admin.site.register(Trips, Trips_Admin)