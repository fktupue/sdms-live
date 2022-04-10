from django.contrib import admin
from .models import User_Account, Company, Farm, Truck, Trips

# Register your models here.

class UserAccount_Admin(admin.ModelAdmin):
    list_display=["user", "first_name", "middle_name", "last_name", "contact_number", "email_address", "profile_pic"]
class Company_Admin(admin.ModelAdmin):
    list_display=["company_name"]
class Farm_Admin(admin.ModelAdmin):
    list_display=["farm_name"]
class Truck_Admin(admin.ModelAdmin):
    list_display=["plate_number", "driver"]
class Trips_Admin(admin.ModelAdmin):
    list_display=["ref_num", "trip_date", "farm", "truck"]

admin.site.register(User_Account, UserAccount_Admin)
admin.site.register(Company, Company_Admin)
admin.site.register(Farm, Farm_Admin)
admin.site.register(Truck, Truck_Admin)
admin.site.register(Trips, Trips_Admin)