from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from .models import Company, Farm, Truck, User_Account, Trips


#User Account

class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #"class": "form-control",
                'type':"text",
                'id' : "username",
                'name' : "username",
                'maxlength' : "50"
            }
        )
    )

    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                #"class": "form-control",
                'type':"password",
                'id' : "password1",
                'name' : "password1",
                'maxlength' : "50",
                'minlength' : "8"
            }
        )
    )

    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                #"class": "form-control",
                'type':"password",
                'id' : "password2",
                'name' : "password2",
                'maxlength' : "50",
                'minlength' : "8"
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm,self).__init__(*args, **kwargs)

class NewUserForm(forms.ModelForm):
    first_name = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #"class": "form_field"
                'type':"text",
                'id' : "fname",
                'name' : "first_name",
                'maxlength' : "50"
            }
        )
    )

    middle_name = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #"class": "form_field"
                'type':"text",
                'id' : "mname",
                'name' : "middle_name",
                'maxlength' : "50"
            }
        )
    )

    last_name = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #"class": "form_field"
                'type':"text",
                'id' : "lname",
                'name' : "last_name",
                'maxlength' : "50"
            }
        )
    )

    contact_number = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #"class": "form_field"
                'type':"text",
                'id' : "contact_num",
                'name' : "contact_number",
                'maxlength' : "15"
            }
        )
    )

    email_address = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #"class": "form_field"
                'type':"text",
                'id' : "email_addrs",
                'name' : "email_address",
                'maxlength' : "50"
            }
        )
    )
    
    profile_pic = forms.ImageField(
        widget = forms.FileInput(
            attrs={
                'type':"file",
                'id':"default-btn",
                'name':"profile_picture",
                'accept':".png,.jpg,.jpeg",
                'hidden':'hidden'
            }
        )
    )

    class Meta:
        model = User_Account
        fields = ['first_name', 'middle_name', 'last_name', 'contact_number', 'email_address', 'profile_pic']

    def __init__(self, *args, **kwargs):
        super(NewUserForm,self).__init__(*args, **kwargs)

class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #"class": "form_field"
                'type':"text",
                'id' : "fname",
                'name' : "first_name",
                'maxlength' : "50"
            }
        )
    )

    middle_name = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #"class": "form_field"
                'type':"text",
                'id' : "mname",
                'name' : "middle_name",
                'maxlength' : "50"
            }
        )
    )

    last_name = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #"class": "form_field"
                'type':"text",
                'id' : "lname",
                'name' : "last_name",
                'maxlength' : "50"
            }
        )
    )

    contact_number = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #"class": "form_field"
                'type':"text",
                'id' : "contact_num",
                'name' : "contact_number",
                'maxlength' : "15"
            }
        )
    )

    email_address = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #"class": "form_field"
                'type':"text",
                'id' : "email_addrs",
                'name' : "email_address",
                'maxlength' : "50"
            }
        )
    )
    
    profile_pic = forms.ImageField(
        widget = forms.FileInput(
            attrs={
                'type':"file",
                'id':"default-btn",
                'name':"profile_picture",
                'accept':".png,.jpg,.jpeg",
                'hidden':'hidden'
            }
        )
    )
    

    class Meta:
        model = User_Account
        fields = ['first_name', 'middle_name', 'last_name', 'contact_number', 'email_address', 'profile_pic']

    def __init__(self, *args, **kwargs):
        super(EditUserForm,self).__init__(*args, **kwargs)

#Edit/Add Items

class NewCompanyForm(forms.ModelForm):
    company_name = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "company-name",
                'name' : "company-name",
                'maxlength' : "50"
            }
        )
    )

    address_line_1 = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "addrs_1",
                'name' : "address-line-1",
                'maxlength' : "60"
            }
        )
    )

    address_line_2 = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "addrs_2",
                'name' : "address-line-2",
                'maxlength' : "60"
            }
        )
    )

    city = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "city",
                'name' : "city",
                'maxlength' : "20"
            }
        )
    )

    province = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "province",
                'name' : "province",
                'maxlength' : "20"
            }
        )
    )

    zip_code = forms.IntegerField(
        widget = forms.NumberInput(
            attrs={
                'type':"number",
                'id' : "zip-code",
                'name' : "zip-code"
            }
        )
    )

    email_address = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "email",
                'name' : "email-address",
                'maxlength' : "50"
            }
        )
    )

    class Meta:
        model = Company
        fields = ["company_name", "address_line_1", "address_line_2", "city", "province", "zip_code", "email_address"]
    
    def __init__(self, *args, **kwargs):
        super(NewCompanyForm,self).__init__(*args, **kwargs)


class NewFarmForm(forms.ModelForm):
    farm_name = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "farm-name",
                'name' : "farm-name",
                'maxlength' : "50"
            }
        )
    )

    address_line_1 = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "address-line-1",
                'name' : "address_line_1",
                'maxlength' : "60"
            }
        )
    )

    address_line_2 = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "address-line-2",
                'name' : "address-line-2",
                'maxlength' : "60"
            }
        )
    )

    city = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "city",
                'name' : "city",
                'maxlength' : "20"
            }
        )
    )

    province = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "province",
                'name' : "province",
                'maxlength' : "20"
            }
        )
    )

    zip_code = forms.IntegerField(
        widget = forms.NumberInput(
            attrs={
                'type':"number",
                'id' : "zip-code",
                'name' : "zip-code"
            }
        )
    )

    distance = forms.DecimalField(
        widget = forms.NumberInput(
            attrs={
                'type':"number",
                'id' : "distance",
                'name' : "distance",
                'step' : '0.1'
            }
        )
    )

    capacity = forms.DecimalField(
        widget = forms.NumberInput(
            attrs={
                'type':"number",
                'id' : "capacity",
                'name' : "capacity",
                'step' : '0.1'
            }
        )
    )

    company = forms.ModelChoiceField(queryset=Company.objects.all(), empty_label=None,
        widget = forms.RadioSelect(
            attrs={
                'type' : "radio",
                'class' : "radio",
                'name' : "category"
            }
        ),
    )

    rate_code = forms.IntegerField(
        widget = forms.NumberInput(
            attrs={
                'type' : "number",
                'id' : "rate-code",
                'name' : "rate-code"
            }
        )
    )

    remarks = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "remarks",
                'name' : "remarks",
                'maxlength' : "150"
            }
        )
    )

    class Meta:
        model = Farm
        fields = ['farm_name', 'address_line_1', 'address_line_2', 'city', 'province', 'zip_code', 'distance', 'capacity', 'company', 'rate_code', 'remarks']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class EditFarmForm(forms.ModelForm):
    farm_name = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "farm-name",
                'name' : "farm-name",
                'maxlength' : "50"
            }
        )
    )

    address_line_1 = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "address-line-1",
                'name' : "address_line_1",
                'maxlength' : "60"
            }
        )
    )

    address_line_2 = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "address-line-2",
                'name' : "address-line-2",
                'maxlength' : "60"
            }
        )
    )

    city = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "city",
                'name' : "city",
                'maxlength' : "20"
            }
        )
    )

    province = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "province",
                'name' : "province",
                'maxlength' : "20"
            }
        )
    )

    zip_code = forms.IntegerField(
        widget = forms.NumberInput(
            attrs={
                'type':"number",
                'id' : "zip-code",
                'name' : "zip-code"
            }
        )
    )

    distance = forms.DecimalField(
        widget = forms.NumberInput(
            attrs={
                'type':"number",
                'id' : "distance",
                'name' : "distance",
                'step' : '0.1'
            }
        )
    )

    capacity = forms.DecimalField(
        widget = forms.NumberInput(
            attrs={
                'type':"number",
                'id' : "capacity",
                'name' : "capacity",
                'step' : '0.1'
            }
        )
    )

    company = forms.ModelChoiceField(queryset=Company.objects.all(), empty_label=None,
        widget = forms.RadioSelect(
            attrs={
                'type' : "radio",
                'class' : "radio",
                'name' : "category"
            }
        ),
    )

    rate_code = forms.IntegerField(
        widget = forms.NumberInput(
            attrs={
                'type' : "number",
                'id' : "rate-code",
                'name' : "rate-code"
            }
        )
    )

    billing_rate_override = forms.DecimalField(
        widget = forms.NumberInput(
            attrs={
                'type':"number",
                'id' : "rate-adjust",
                'name' : "rate_adjust",
                'step' : '0.01'
            }
        )
    )

    remarks = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "remarks",
                'name' : "remarks",
                'maxlength' : "150"
            }
        )
    )

    class Meta:
        model = Farm
        fields = ['farm_name', 'address_line_1', 'address_line_2', 'city', 'province', 'zip_code', 'distance', 'capacity', 'company', 'rate_code', 'billing_rate_override', 'remarks']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NewTruckForm(forms.ModelForm):
    plate_number = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "plate_number",
                'name' : "plate-number",
                'maxlength' : "10"
            }
        )
    )

    truck_cat = [
        ('ELF', 'ELF'),
        ('FWD', 'FWD'),
        ('PFWD-1', 'PFWD-1'),
        ('PFWD-2', 'PFWD-2'),
        ('SEMI PFWD', 'SEMI PFWD')
    ]
    
    truck_classification = forms.ChoiceField(choices=truck_cat,
        widget = forms.RadioSelect(
            attrs={
                'type' : "radio",
                'class' : "radio",
                'name' : "truck_classification"
            }
        ),
    )

    driv = User_Account.objects.filter(Q(user__groups__name__icontains="Driver", visible="SHOW")).select_related('user')
    trucks = Truck.objects.filter(driver__in=driv)
    ids = []
    for d in trucks:
        a = d.driver
        b = a.id
        ids.append(int(b))
    available_drivers = User_Account.objects.exclude(Q(id__in=ids) | Q(user__groups__name="Admin") | Q(user__groups__name="Management") | Q(user__groups__name="Staff") | Q(visible="HIDE"))

    driver = forms.ModelChoiceField(queryset=available_drivers, empty_label=None,
        widget = forms.RadioSelect(
            attrs={
                'type' : "radio-2",
                'class' : "radio-2",
                'name' : "driver"
            }
        ),
    )

    company = forms.ModelChoiceField(queryset=Company.objects.all(), empty_label=None,
        widget = forms.RadioSelect(
            attrs={
                'type' : "radio-3",
                'class' : "radio-3",
                'name' : "company"
            }
        ),
    )

    class Meta:
        model = Truck
        fields = ['plate_number', 'truck_classification', 'driver', 'company']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NewTrip(forms.ModelForm):
    get_farms = Farm.objects.all()
    get_trucks = Truck.objects.all()

    farm = forms.ModelChoiceField(queryset=get_farms, empty_label=None,
        widget = forms.RadioSelect(
            attrs={
                'type' : "radio",
                'class' : "radio",
                'name' : "farm"
            }
        ),
    )

    truck = forms.ModelChoiceField(queryset=get_trucks, empty_label=None,
        widget = forms.RadioSelect(
            attrs={
                'type' : "radio-2",
                'class' : "radio-2",
                'name' : "truck"
            }
        ),
    )
    
    trip_date = forms.DateField(
        widget = forms.DateInput(
            format=("%Y-%m-%d"),
            attrs={
                'type' : "date",
                'id' : "trip-date",
                'name' : "trip-date"
            }
        )
    )
    

    bag_count = forms.IntegerField(
        widget = forms.NumberInput(
            attrs={
                'type' : "number",
                'id' : "bag-count",
                'name' : "bag-count"
            }
        )
    )

    helper_1 = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "helper-1",
                'name' : "helper-1",
                'maxlength' : "30"
            }
        )
    )

    helper_2 = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "helper-2",
                'name' : "helper-2",
                'maxlength' : "30"
            }
        )
    )

    helper_3 = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "helper-3",
                'name' : "helper-3",
                'maxlength' : "30"
            }
        )
    )


    class Meta:
        model = Trips
        fields = ['farm', 'truck', 'trip_date', 'bag_count', 'helper_1', 'helper_2', 'helper_3']

    def __init__(self, *args, **kwargs):
        super(NewTrip,self).__init__(*args, **kwargs)
        # self.fields['helper_1'].required = False
        # self.fields['helper_2'].required = False
        # self.fields['helper_3'].required = False

class EditTrip_management(forms.ModelForm):
    bag_count = forms.IntegerField(
        widget = forms.NumberInput(
            attrs={
                'type' : "number",
                'id' : "bag-count",
                'name' : "bag-count"
            }
        )
    )
    
    rate_adjustment = forms.DecimalField(
        widget = forms.NumberInput(
            attrs={
                'type':"number",
                'id' : "rate-adjust",
                'name' : "rate_adjust",
                'step' : '0.01'
            }
        )
    )

    management_remarks = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #"class": "form_field"
                'type':"text",
                'id' : "management-remarks",
                'name' : "management_remarks",
                'maxlength' : "100"
            }
        )
    )

    class Meta:
        model = Trips
        fields = ['bag_count', 'rate_adjustment', 'management_remarks']

    def __init__(self, *args, **kwargs):
        super(EditTrip_management,self).__init__(*args, **kwargs)

class EditTrip_staff(forms.ModelForm):
    tripstatus = [
        ('IN PROGRESS', 'IN PROGRESS'),
        ('DELIVERED', 'DELIVERED')
    ]

    paystatus = [
        ('PAID', 'PAID')
    ]

    trip_status = forms.ChoiceField(choices=tripstatus,
        widget = forms.RadioSelect(
            attrs={
                'type' : "radio",
                'class' : "radio",
                'name' : "trip-status"
            }
        ),
    )

    payment_status = forms.ChoiceField(choices=paystatus,
        widget = forms.RadioSelect(
            attrs={
                'type' : "radio-2",
                'class' : "radio-2",
                'name' : "payment-status"
            }
        ),
    )

    bag_count = forms.IntegerField(
        widget = forms.NumberInput(
            attrs={
                'type' : "number",
                'id' : "bag-count",
                'name' : "bag-count"
            }
        )
    )

    driver_additional = forms.DecimalField(
        widget = forms.NumberInput(
            attrs={
                'type':"number",
                'id' : "driver-addtnl",
                'name' : "driver_addtnl",
                'step' : '0.01'
            }
        )
    )

    driver_additional_remarks = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #"class": "form_field"
                'type':"text",
                'id' : "management-remarks",
                'name' : "management_remarks",
                'maxlength' : "100"
            }
        )
    )

    class Meta:
        model = Trips
        fields = ['trip_status', 'payment_status', 'bag_count', 'driver_additional', 'driver_additional_remarks']

    def __init__(self, *args, **kwargs):
        super(EditTrip_staff,self).__init__(*args, **kwargs)
        self.fields['trip_status'].required = False
        self.fields['payment_status'].required = False

class EditTrip_driver(forms.ModelForm):
    tripstatus = [
        ('DELIVERED', 'DELIVERED')
    ]

    trip_status = forms.ChoiceField(choices=tripstatus,
        widget = forms.RadioSelect(
            attrs={
                'type' : "radio",
                'class' : "radio",
                'name' : "trip-status"
            }
        ),
    )

    bag_count = forms.IntegerField(
        widget = forms.NumberInput(
            attrs={
                'type' : "number",
                'id' : "bag-count",
                'name' : "bag-count"
            }
        )
    )

    additional_expense = forms.DecimalField(
        widget = forms.NumberInput(
            attrs={
                'type':"number",
                'id' : "driver-addtnl",
                'name' : "driver_addtnl",
                'step' : '0.01'
            }
        )
    )

    additional_expense_remark = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #"class": "form_field"
                'type':"text",
                'id' : "management-remarks",
                'name' : "management_remarks",
                'maxlength' : "100"
            }
        )
    )

    class Meta:
        model = Trips
        fields = ['trip_status', 'bag_count', 'additional_expense', 'additional_expense_remark']

    def __init__(self, *args, **kwargs):
        super(EditTrip_driver,self).__init__(*args, **kwargs)
        self.fields['trip_status'].required = False

class NewTrip_driver(forms.ModelForm):
    get_farms = Farm.objects.all()

    farm = forms.ModelChoiceField(queryset=get_farms, empty_label=None,
        widget = forms.RadioSelect(
            attrs={
                'type' : "radio",
                'class' : "radio",
                'name' : "farm"
            }
        ),
    )
    
    trip_date = forms.DateField(
        widget = forms.DateInput(
            format=("%Y-%m-%d"),
            attrs={
                'type' : "date",
                'id' : "trip-date",
                'name' : "trip-date"
            }
        )
    )

    bag_count = forms.IntegerField(
        widget = forms.NumberInput(
            attrs={
                'type' : "number",
                'id' : "bag-count",
                'name' : "bag-count"
            }
        )
    )

    helper_1 = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "helper-1",
                'name' : "helper-1",
                'maxlength' : "30"
            }
        )
    )

    helper_2 = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "helper-2",
                'name' : "helper-2",
                'maxlength' : "30"
            }
        )
    )

    helper_3 = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':"text",
                'id' : "helper-3",
                'name' : "helper-3",
                'maxlength' : "30"
            }
        )
    )


    class Meta:
        model = Trips
        fields = ['farm', 'trip_date', 'bag_count', 'helper_1', 'helper_2', 'helper_3']

    def __init__(self, *args, **kwargs):
        super(NewTrip_driver,self).__init__(*args, **kwargs)
        # self.fields['helper_1'].required = False
        # self.fields['helper_2'].required = False
        # self.fields['helper_3'].required = False