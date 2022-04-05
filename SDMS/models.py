from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.conf import settings

# Create your models here.

class User_Account(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    email_address = models.CharField(max_length=50)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='files/pfp', default=None)
    accnt_status = models.CharField(max_length=50, default='OFFLINE')
    visible = models.CharField(max_length=10, default='SHOW')

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

class Activity_Log(models.Model):
    user = models.ForeignKey(User_Account, on_delete=models.CASCADE)
    action = models.CharField(max_length=40)
    activity_date = models.DateTimeField(auto_now_add=True)

class Company(models.Model):
    company_name = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=60)
    address_line_2 = models.CharField(max_length=60)
    city = models.CharField(max_length=20)
    province = models.CharField(max_length=20)
    zip_code = models.IntegerField()
    email_address = models.CharField(max_length=50)
    visible = models.CharField(max_length=10, default='SHOW')

    def __str__(self):
        return str(self.company_name)

class Farm(models.Model):
    farm_name = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=60)
    address_line_2 = models.CharField(max_length=60)
    city = models.CharField(max_length=20)
    province = models.CharField(max_length=20)
    zip_code = models.IntegerField()
    distance = models.DecimalField(decimal_places=1, max_digits=6)
    capacity = models.DecimalField(decimal_places=1, max_digits=6)
    rate_code = models.IntegerField()
    remarks = models.CharField(max_length=150)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    visible = models.CharField(max_length=10, default='SHOW')

    def __str__(self):
        return str(self.farm_name)

class Truck(models.Model):
    plate_number = models.CharField(max_length=10)
    truck_classification = models.CharField(max_length=20)
    capacity = models.IntegerField(default=0)
    driver = models.ForeignKey(User_Account, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    visible = models.CharField(max_length=10, default='SHOW')

    def __str__(self):
        return str(self.plate_number) + ' (' + str(self.truck_classification) + ')'

class Trips(models.Model):
    start_time = models.DateTimeField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    last_edit_by = models.ForeignKey(User_Account, on_delete=models.CASCADE, null=True)
    ref_num = models.CharField(max_length=10, blank=True, null=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, null=True)
    trip_date = models.DateField()
    bag_count = models.IntegerField()
    driver_basic = models.IntegerField(default=0)
    driver_additional = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    helper_1 = models.CharField(max_length=30, blank=True, null=True)
    helper_2 = models.CharField(max_length=30, blank=True, null=True)
    helper_3 = models.CharField(max_length=30, blank=True, null=True)
    helper1_basic = models.IntegerField(default=0)
    helper2_basic = models.IntegerField(default=0)
    helper3_basic = models.IntegerField(default=0)
    base_rate = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    additional_expense = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    rate_adjustment = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    management_remarks = models.CharField(max_length=100, blank=True, null=True)
    trip_status = models.CharField(max_length=20, default="SCHEDULED")
    payment_status = models.CharField(max_length=20, default="UNPAID")

    def __str__(self):
        return str(self.id)

class Driver_FinancialReport(models.Model):
    driver = models.ForeignKey(User_Account, on_delete=models.CASCADE)
    trip_month = models.IntegerField()
    trip_year = models.IntegerField()
    trip_count = models.IntegerField(default=0)
    bag_count = models.IntegerField(default=0)
    driver_basic = models.IntegerField(default=0)
    driver_additional = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

class Client_FinancialReport(models.Model):
    client = models.ForeignKey(Company, on_delete=models.CASCADE)
    trip_month = models.IntegerField(default=0)
    trip_year = models.IntegerField(default=0)
    trip_inprogress = models.IntegerField(default=0)
    trip_completed = models.IntegerField(default=0)
    bag_count = models.IntegerField(default=0)
    base_rate = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    rate_adjust = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)