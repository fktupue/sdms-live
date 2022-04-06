from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Sum
from django.db.models import Q
from datetime import date, datetime
from time import gmtime, strftime
from django.http import JsonResponse, HttpResponse, FileResponse
import string, random, json, csv
from django.template.loader import get_template
from xhtml2pdf import pisa
from django_user_agents.utils import get_user_agent
from decimal import Decimal

from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import SignUpForm, LoginForm, EditUserForm, NewCompanyForm, NewFarmForm, NewTruckForm, NewTrip, EditTrip_management, EditTrip_staff, EditTrip_driver, NewTrip_driver
from .models import User_Account, Company, Farm, Truck, Trips, Activity_Log, Driver_FinancialReport, Client_FinancialReport
from .utils import render_to_pdf

#reference number generator
def generate_refno():
    ref_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    return ref_no

#generate csv
@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Management'])
def generate_report(request):
    if request.method == "GET":
        response = HttpResponse(content_type='text/csv')
        trips = Trips.objects.all().order_by('trip_date')
        data = trips.values_list('ref_num', 'trip_date', 'farm__company__company_name', 'farm__farm_name', 'farm__address_line_1', 'farm__address_line_2', 'farm__city',
        'farm__province', 'farm__distance', 'farm__rate_code', 'truck__plate_number', 'truck__capacity', 'bag_count', 'truck__driver__last_name',
        'driver_basic', 'driver_additional', 'helper_1', 'helper1_basic', 'helper_2', 'helper2_basic', 'helper_3', 'helper3_basic', 'rate_adjustment', 'management_remarks')
        writer = csv.writer(response)
        writer.writerow(['Reference Number', 'Trip Date', 'Account', 'Farm', 'Address Line 1', 'Address Line 2', 'City', 'Province', 'Distance', 'Rate Code', 'Truck', 'Capacity', 'Bags Delivered', 
        'Driver', 'Driver Basic', 'Driver Additional', 'Helper 1', 'Helper 1 Basic', 'Helper 2', 'Helper 2 Basic', 'Helper 3', 'Helper 3 Basic', 'Rate Adjustment', 'Remarks'])
        for detail in data:
            writer.writerow(detail)
        filename = 'sdms-tripreport-' + str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
        response['Content-Disposition'] = 'attachment; filename=' + filename + '.csv'
        return response

#generate pdf
@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Management'])
def generate_financialreport(request, id):
    if request.method == 'GET':
        client_details = Company.objects.get(pk=id)
        total = 0
        all_trips = Trips.objects.filter(farm__company__id=client_details.id, trip_date__month=datetime.today().month, trip_date__year=datetime.today().year)
        for i in all_trips:
            total += i.base_rate
        data = {
            'month' : str(datetime.today().strftime("%B")),
            'year' : str(datetime.today().year),
            'client_name' : client_details.company_name,
            'client_address' : client_details.address_line_1 + ' ' + client_details.address_line_2 + ' ' + client_details.city + ' ' + client_details.province + ' ' + str(client_details.zip_code),
            'client_email' : client_details.email_address,
            'client_trips' : all_trips,
            'total_due' : str(total),
        }
        pdf = render_to_pdf('financial_report.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'Financial-Report-' + client_details.company_name + '-' + str(datetime.today().strftime("%b")) + '-' + str(datetime.today().year)
        content = "attachment; filename=" + (filename)
        response['Content-Disposition'] = content
        return response

#Search function
def search_client(request):
    if request.method == "POST":
        search_str=json.loads(request.body).get('textSearch')
        clients = Company.objects.filter(company_name__istartswith=search_str, visible='SHOW')
        data = clients.values()
        return JsonResponse(list(data), safe=False)

def search_farm(request):
    if request.method == "POST":
        search_str=json.loads(request.body).get('textSearch')
        farms = Farm.objects.filter(Q(farm_name__istartswith=search_str, visible='SHOW')|Q(rate_code__istartswith=search_str, visible='SHOW')|Q(capacity__istartswith=search_str, visible='SHOW')|Q(company__company_name__istartswith=search_str, visible='SHOW')).select_related('company')
        data = farms.values('farm_name', 'address_line_1', 'address_line_2', 'city', 'province', 'zip_code', 'distance', 'capacity', 'rate_code', 'remarks', 'company__company_name', 'id')
        return JsonResponse(list(data), safe=False)

def search_truck(request):
    if request.method == "POST":
        search_str=json.loads(request.body).get('textSearch')
        trucks = Truck.objects.filter(Q(plate_number__icontains=search_str, visible='SHOW')|Q(truck_classification__istartswith=search_str, visible='SHOW')|Q(capacity__istartswith=search_str, visible='SHOW')|Q(driver__last_name__istartswith=search_str, visible='SHOW')|Q(company__company_name__istartswith=search_str, visible='SHOW')).select_related('driver').select_related('company')
        data = trucks.values('plate_number', 'truck_classification', 'capacity', 'driver__first_name', 'driver__last_name', 'company__company_name', 'id')
        return JsonResponse(list(data), safe=False)

def search_user(request):
    if request.method == 'POST':
        search_str=json.loads(request.body).get('textSearch')
        users = User_Account.objects.filter(Q(last_name__icontains=search_str, visible='SHOW')|Q(first_name__icontains=search_str, visible='SHOW')|Q(user__groups__name__istartswith=search_str, visible='SHOW')|Q(email_address__istartswith=search_str, visible='SHOW')).select_related('user').order_by('user__groups__name')
        data = users.values('id', 'first_name', 'last_name', 'contact_number', 'email_address', 'user__groups__name', 'profile_pic')
        return JsonResponse(list(data), safe=False)

def search_trip(request):
    if request.method == "POST":
        search_str=json.loads(request.body).get('textSearch')
        try:
            get_dates = search_str.split(':')
            date1 = get_dates[0].split("-")
            date2 = get_dates[1].split("-")
            trucks = Trips.objects.filter(Q(trip_date__range=[date(int(date1[0]), int(date1[1]), int(date1[2])), date(int(date2[0]), int(date2[1]), int(date2[2]))])).select_related('truck').select_related('farm').order_by('trip_date')
        except IndexError:
            trucks = Trips.objects.filter(Q(ref_num__istartswith=search_str)|
            Q(trip_date__icontains=search_str)|Q(truck__plate_number__istartswith=search_str)|
            Q(truck__driver__last_name__istartswith=search_str)|Q(truck__driver__first_name__istartswith=search_str)|Q(farm__farm_name__istartswith=search_str)|
            Q(farm__company__company_name__istartswith=search_str)|Q(trip_status__icontains=search_str)|
            Q(payment_status__icontains=search_str)|Q(bag_count__istartswith=search_str)).select_related('truck').select_related('farm').order_by('trip_date')
        data = trucks.values('ref_num', 'trip_date', 'truck__plate_number', 'truck__truck_classification',
        'truck__driver__first_name', 'truck__driver__last_name', 'farm__farm_name', 'farm__company__company_name', 
        'trip_status', 'payment_status', 'bag_count', 'id')
        return JsonResponse(list(data), safe=False)

def driver_search_trip(request):
    if request.method == "POST":
        search_str=json.loads(request.body).get('textSearch')
        try:
            get_dates = search_str.split(':')
            date1 = get_dates[0].split("-")
            date2 = get_dates[1].split("-")
            trucks = Trips.objects.filter(Q(truck__driver__user=request.user.id, trip_date__range=[date(int(date1[0]), int(date1[1]), int(date1[2])), date(int(date2[0]), int(date2[1]), int(date2[2]))])).select_related('truck').select_related('farm').order_by('trip_date')
        except IndexError:
            trucks = Trips.objects.filter(Q(truck__driver__user=request.user.id, ref_num__istartswith=search_str)|
            Q(truck__driver__user=request.user.id, trip_date__icontains=search_str)|Q(truck__driver__user=request.user.id, truck__plate_number__istartswith=search_str)|
            Q(truck__driver__user=request.user.id, truck__driver__last_name__istartswith=search_str)|Q(truck__driver__user=request.user.id, truck__driver__first_name__istartswith=search_str)|Q(truck__driver__user=request.user.id, farm__farm_name__istartswith=search_str)|
            Q(truck__driver__user=request.user.id, farm__company__company_name__istartswith=search_str)|Q(truck__driver__user=request.user.id, trip_status__icontains=search_str)|
            Q(truck__driver__user=request.user.id, payment_status__icontains=search_str)|Q(truck__driver__user=request.user.id, bag_count__istartswith=search_str)).select_related('truck').select_related('farm').order_by('trip_date')
        data = trucks.values('ref_num', 'trip_date', 'truck__plate_number', 'truck__truck_classification',
        'truck__driver__first_name', 'truck__driver__last_name', 'farm__farm_name', 'farm__company__company_name', 
        'trip_status', 'payment_status', 'bag_count', 'id')
        return JsonResponse(list(data), safe=False)

# Create your views here.
@unauthenticated_user
def login_user(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                admin_group = Group(name="Admin")
                management_group = Group(name="Management")
                staff_group = Group(name="Staff")
                driver_group = Group(name="Driver")
                if user.groups.filter(name=admin_group):
                    return redirect('SDMS:superuser-home')
                if user.groups.filter(name=management_group):
                    get_account = User_Account.objects.get(user=user)
                    get_account.accnt_status = 'ONLINE'
                    get_account.save()
                    return redirect('SDMS:management-home')
                if user.groups.filter(name=staff_group):
                    get_account = User_Account.objects.get(user=user)
                    get_account.accnt_status = 'ONLINE'
                    get_account.save()
                    return redirect('SDMS:staff-home')
                if user.groups.filter(name=driver_group):
                    get_account = User_Account.objects.get(user=user)
                    get_account.accnt_status = 'ONLINE'
                    get_account.save()
                    return redirect('SDMS:driver-home')
            else: 
                msg = 'Invalid username or password'
        else:
            msg = "Validation error"
    context = {'form' : form, 'msg' : msg}
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, "mobile/login.html", context)
    else:
        return render(request, "login.html", context)

def logout_user(request):
    try:
        check_account = User_Account.objects.get(user=request.user.id)
        check_role = User.objects.get(id=check_account.user_id)
        management_group = Group(name="Management")
        staff_group = Group(name="Staff")
        driver_group = Group(name="Driver")
        if check_role.groups.filter(name=management_group):
            check_account.accnt_status = 'OFFLINE'
            check_account.save()
        if check_role.groups.filter(name=staff_group):
            check_account.accnt_status = 'OFFLINE'
            check_account.save()
        if check_role.groups.filter(name=driver_group):
            check_account.accnt_status = 'OFFLINE'
            check_account.save()
        logout(request)
    except User_Account.DoesNotExist:
        logout(request)
    return redirect('SDMS:login')


#SUPERUSER
@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_home(request):
    online_count = 0
    active_count = 0
    online = User_Account.objects.all()
    trips = Trips.objects.all().order_by('trip_date')
    for i in online:
        if i.accnt_status == "ONLINE":
            online_count += 1
    for t in trips:
        if t.trip_status == "SCHEDULED":
            active_count += 1
        if t.trip_status == "IN PROGRESS":
            active_count += 1
    context = {'screen_name' : "Home",
        "online_users" : online_count,
        "active_trips" : active_count,
        "trips" : trips
    }
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, "mobile/superuser_home.html", context)
    else:
        return render(request, "superuser_home.html", context)

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_edittrip(request, id=0):
    ref_no = None
    trip_id = 0
    current_bagcount = 0
    current_farm = None
    current_truck = None
    if request.method == "GET":
        if id == 0:
            form = NewTrip()
        else:
            trip = Trips.objects.get(id=id)
            ref_no = trip.ref_num
            trip_id += trip.id
            current_bagcount += trip.bag_count
            current_farm = trip.farm
            current_truck = trip.truck
            form = NewTrip(instance=trip)
        context = {'form' : form,
            'screen_name' : 'New Trip',
            'reference_number' : ref_no,
            'current_farm' : current_farm,
            'current_truck' : current_truck
        }
        if request.user_agent.is_mobile or request.user_agent.is_tablet:
            return render(request, "mobile/superuser_edittrip.html", context)
        else:
            return render(request, "superuser_edittrip.html", context)
    if request.method == "POST":
        if id == 0:
            form = NewTrip(request.POST)
        else:
            trip = Trips.objects.get(pk=id)
            trip_id += trip.id
            form = NewTrip(request.POST, request.FILES, instance=trip)
        state = 0
        if form.is_valid():
            form.save()
            state += 1
            if state == 1:
                get_farm_form = request.POST.get('farm')
                get_truck_form = request.POST.get('truck')
                farm_data = Farm.objects.get(id=get_farm_form)
                truck_data = Truck.objects.get(id=get_truck_form)
                distance_class = 0
                driver_basic = 0
                helper1_basic = 0
                helper2_basic = 0
                helper3_basic = 0
                if 0 <= farm_data.distance <= 40:
                    distance_class += 1
                if 41 <= farm_data.distance <= 80:
                    distance_class += 2
                if 81 <= farm_data.distance <= 120:
                    distance_class += 3
                if 121 <= farm_data.distance <= 160:
                    distance_class += 4
                if 161 <= farm_data.distance <= 200:
                    distance_class += 5
                if 201 <= farm_data.distance <= 240:
                    distance_class += 6
                if farm_data.distance == 310:
                    distance_class += 430
                if farm_data.distance == 340:
                    distance_class += 675
                if distance_class == 1 and truck_data.truck_classification == 'ELF':
                    driver_basic += 280
                    helper1_basic += 180
                    helper2_basic += 180
                    helper3_basic += 180
                if distance_class == 1 and truck_data.truck_classification == 'FWD':
                    driver_basic += 330
                    
                    helper1_basic += 250
                
                    helper2_basic += 250
                
                    helper3_basic += 250
                if distance_class == 1 and truck_data.truck_classification == 'PFWD-1':
                    driver_basic += 430
                    
                    helper1_basic += 330
                
                    helper2_basic += 330
                
                    helper3_basic += 330
                if distance_class == 1 and truck_data.truck_classification == 'PFWD-2':
                    driver_basic += 530
                    
                    helper1_basic += 280
                
                    helper2_basic += 280
                
                    helper3_basic += 280
                if distance_class == 2 and truck_data.truck_classification == 'ELF':
                    driver_basic += 330
                    
                    helper1_basic += 180
                
                    helper2_basic += 180
                
                    helper3_basic += 180
                if distance_class == 2 and truck_data.truck_classification == 'FWD':
                    driver_basic += 430
                    
                    helper1_basic += 250
                
                    helper2_basic += 250
                
                    helper3_basic += 250
                if distance_class == 2 and truck_data.truck_classification == 'PFWD-1':
                    driver_basic += 580
                    
                    helper1_basic += 330
                
                    helper2_basic += 330
                
                    helper3_basic += 330
                if distance_class == 2 and truck_data.truck_classification == 'PFWD-2':
                    driver_basic += 730
                    
                    helper1_basic += 280
                
                    helper2_basic += 280
                
                    helper3_basic += 280
                if distance_class == 3 and truck_data.truck_classification == 'ELF':
                    driver_basic += 380
                    
                    helper1_basic += 200
                
                    helper2_basic += 200
                
                    helper3_basic += 200
                if distance_class == 3 and truck_data.truck_classification == 'FWD':
                    driver_basic += 500
                    
                    helper1_basic += 280
                
                    helper2_basic += 280
                
                    helper3_basic += 280 
                if distance_class == 3 and truck_data.truck_classification == 'PFWD-1':
                    driver_basic += 675
                    
                    helper1_basic += 380
                
                    helper2_basic += 380
                
                    helper3_basic += 380
                if distance_class == 3 and truck_data.truck_classification == 'PFWD-2':
                    driver_basic += 850
                    
                    helper1_basic += 320
                
                    helper2_basic += 320
                
                    helper3_basic += 320
                if distance_class == 4 and truck_data.truck_classification == 'ELF':
                    driver_basic += 430
                    
                    helper1_basic += 200
                
                    helper2_basic += 200
                
                    helper3_basic += 200
                if distance_class == 4 and truck_data.truck_classification == 'FWD':
                    driver_basic += 550
                    
                    helper1_basic += 280
                
                    helper2_basic += 280
                
                    helper3_basic += 280 
                '''
                if distance_class == 4 and truck_data.truck_classification == 'PFWD-1':
                    driver_basic += 675
                    
                    helper1_basic += 380
                
                    helper2_basic += 380
                
                    helper3_basic += 380
                if distance_class == 4 and truck_data.truck_classification == 'PFWD-2':
                    driver_basic += 850
                    
                    helper1_basic += 320
                
                    helper2_basic += 320
                
                    helper3_basic += 320
                '''
                if distance_class == 5 and truck_data.truck_classification == 'ELF':
                    driver_basic += 480
                    
                    helper1_basic += 215
                
                    helper2_basic += 215
                
                    helper3_basic += 215
                if distance_class == 5 and truck_data.truck_classification == 'FWD':
                    driver_basic += 600
                    
                    helper1_basic += 310
                
                    helper2_basic += 310
                
                    helper3_basic += 310
                if distance_class == 6 and truck_data.truck_classification == 'ELF':
                    driver_basic += 530
                    
                    helper1_basic += 215
                
                    helper2_basic += 215
                
                    helper3_basic += 215
                if distance_class == 6 and truck_data.truck_classification == 'FWD':
                    driver_basic += 650
                    
                    helper1_basic += 310
                
                    helper2_basic += 310
                
                    helper3_basic += 310
                trip = Trips.objects.get(id=trip_id)
                trip.driver_basic = driver_basic
                trip.helper1_basic = helper1_basic
                trip.helper2_basic = helper2_basic
                trip.helper3_basic = helper3_basic
                trip.save()
                get_truck = Truck.objects.get(id=trip.truck.id)
                capacity = get_truck.capacity
                driver_findata = Driver_FinancialReport.objects.get(driver__id=trip.truck.driver.id, trip_month=int(trip.trip_date.month), trip_year=(trip.trip_date.year))
                client_findata = Client_FinancialReport.objects.get(client__id=trip.farm.company.id, trip_month=int(trip.trip_date.month), trip_year=(trip.trip_date.year))
                if current_bagcount > trip.bag_count:
                    current_bagcount -= trip.bag_count
                    driver_findata.bag_count = current_bagcount
                    client_findata.bag_count = current_bagcount
                if current_bagcount < trip.bag_count:
                    current_bagcount += trip.bag_count
                    driver_findata.bag_count = current_bagcount
                    client_findata.bag_count = current_bagcount
                if trip.bag_count < (capacity * 0.70):
                    client_findata.base_rate += (Decimal(capacity * 0.70) * trip.farm.rate_code)
                else:
                    client_findata.base_rate += (trip.bag_count * trip.farm.rate_code)
                driver_findata.save()
                client_findata.save()
        return redirect('SDMS:superuser-home')

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_deletetrip(request, id):
    trip = Trips.objects.get(pk=id)
    driver_findata = Driver_FinancialReport.objects.get(driver_id=trip.truck.driver.id, trip_month=int(trip.trip_date.month), trip_year=int(trip.trip_date.year))
    client_findata = Client_FinancialReport.objects.get(client_id=trip.farm.company.id, trip_month=int(trip.trip_date.month), trip_year=int(trip.trip_date.year))
    if trip.trip_status == 'SCHEDULED' or trip.trip_status == 'IN PROGRESS':
        client_findata.trip_inprogress -= 1
    if trip.trip_status == 'DELIVERED':
        client_findata.trip_completed -= 1
    driver_findata.trip_count -= 1
    driver_findata.bag_count -= trip.bag_count
    driver_findata.driver_basic -= trip.driver_basic
    driver_findata.driver_additional -= trip.driver_additional
    client_findata.bag_count -= trip.bag_count
    client_findata.base_rate -= trip.base_rate
    client_findata.rate_adjust -= trip.rate_adjustment
    driver_findata.save()
    client_findata.save()
    trip.delete()
    return redirect('SDMS:superuser-home')

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_calendar(request):
    context = {'screen_name' : "Calendar"}
    return render(request, "superuser_calendar.html", context)

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_clientdata(request):
    clients = Company.objects.filter(visible='SHOW')
    context = {'screen_name' : "Client Data",
    'clients' : clients
    }
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, "mobile/superuser_clients.html", context)
    else:
        return render(request, "superuser_clientdata.html", context)

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_clientdelete(request, id):
    client = Company.objects.get(pk=id)
    client.visible = 'HIDE'
    client.save()
    return redirect('SDMS:superuser-clientdata')

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_farmdata(request):
    farms = Farm.objects.filter(visible='SHOW')
    context = {'screen_name' : "Farm Data",
    'farms' : farms
    }
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, "mobile/superuser_farmdata.html", context)
    else:
        return render(request, "superuser_farmdata.html", context)

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_farmdelete(request, id):
    farm = Farm.objects.get(pk=id)
    farm.visible = 'HIDE'
    farm.save()
    return redirect('SDMS:superuser-farmdata')

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_truckdata(request):
    trucks = Truck.objects.filter(visible='SHOW')
    context = {'screen_name' : "Truck Data",
    'trucks' : trucks
    }
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, "mobile/superuser_truckdata.html", context)
    else:
        return render(request, "superuser_truckdata.html", context)

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_truckdelete(request, id):
    truck = Truck.objects.get(pk=id)
    truck.visible = 'HIDE'
    truck.save()
    return redirect('SDMS:superuser-truckdata')

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_newcompany(request, id=0):
    if request.method == "GET":
        client=None
        screen = None
        if id == 0:
            form = NewCompanyForm()
            screen = 'New Company'
        else:
            client = Company.objects.get(pk=id)
            form = NewCompanyForm(instance=client)
            screen = 'Edit Company'
        context = {'form' : form,
            'screen_name' : 'Company',
            'client' : client,
            'screen' : screen
            }
        if request.user_agent.is_mobile or request.user_agent.is_tablet:
            return render(request, "mobile/superuser_newclient.html", context)
        else:
            return render(request, "superuser_newcompany.html", context)
    if request.method == "POST":
        if id == 0:
            form = NewCompanyForm(request.POST)
        else:
            client = Company.objects.get(pk=id)
            form = NewCompanyForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
        return redirect('SDMS:superuser-clientdata')

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_newfarm(request, id=0):
    farm=None
    company = None
    screen = None
    if request.method == "GET":
        if id == 0:
            form = NewFarmForm()
            company = 'Select Company'
            screen = 'New Farm'
        else:
            farm = Farm.objects.get(pk=id)
            form = NewFarmForm(instance=farm)
            company = farm.company
            screen = 'Edit Farm'
        context = {'form' : form,
            'screen_name' : 'Farm',
            'client' : farm,
            'company' : company,
            'screen' : screen
            }
        if request.user_agent.is_mobile or request.user_agent.is_tablet:
            return render(request, "mobile/superuser_newfarm.html", context)
        else:
            return render(request, "superuser_newfarm.html", context)
    if request.method == "POST":
        if id == 0:
            form = NewFarmForm(request.POST)
        else:
            farm = Farm.objects.get(pk=id)
            form = NewFarmForm(request.POST, request.FILES, instance=farm)
        if form.is_valid():
            form.save()     
        return redirect('SDMS:superuser-farmdata')

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_newtruck(request, id=0):
    truck=None
    category = None
    driver = None
    company = None
    screen = None
    if request.method == "GET":
        if id == 0:
            form = NewTruckForm()
            category = 'Select Category'
            driver = 'Select Driver'
            company = 'Select Company'
            screen = 'New Truck'
        else:
            truck = Truck.objects.get(pk=id)
            form = NewTruckForm(instance=truck)
            category = truck.truck_classification
            driver = truck.driver
            company = truck.company
            screen = 'Edit Truck'
        context = {'form' : form,
            'screen_name' : 'Truck',
            'truck' : truck,
            'category' : category,
            'driver' : driver,
            'company' : company,
            'screen' : screen
        }
        if request.user_agent.is_mobile or request.user_agent.is_tablet:
            return render(request, "mobile/superuser_newtruck.html", context)
        else:
            return render(request, "superuser_newtruck.html", context)
    if request.method == "POST":
        if id == 0:
            form = NewTruckForm(request.POST)
        else:
            truck = Truck.objects.get(pk=id)
            form = NewTruckForm(request.POST, request.FILES, instance=truck)
        if form.is_valid():
            form.save()
            get_truck = request.POST.get('plate_number')
            capacity = 0
            update_capacity = Truck.objects.get(plate_number=get_truck)
            if update_capacity.truck_classification == 'ELF':
                capacity += 150
            if update_capacity.truck_classification == 'ONER':
                capacity += 0
            if update_capacity.truck_classification == 'FWD':
                capacity += 200
            if update_capacity.truck_classification == 'PFWD-1':
                capacity += 280
            if update_capacity.truck_classification == 'PFWD-2':
                capacity += 350
            if update_capacity.truck_classification == 'SEMI PFWD':
                capacity += 0
            update_capacity.capacity = capacity
            update_capacity.save()
        return redirect('SDMS:superuser-truckdata')

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_users(request):
    users = User_Account.objects.filter(visible='SHOW').order_by('user__groups__name')
    context = {'screen_name' : "Users",
    'users' : users
    }
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, "mobile/superuser_users.html", context)
    else:
        return render(request, "superuser_users.html", context) 

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_edituser(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = EditUserForm()
        else:
            user = User_Account.objects.get(pk=id)
            form = EditUserForm(instance=user)
            context= {'form' : form,
                'screen_name' : 'Edit User',
                'user' : user}
        if request.user_agent.is_mobile or request.user_agent.is_tablet:
            return render(request, "mobile/superuser_edituser.html", context)
        else:
            return render(request, "superuser_edituser.html", context)
    if request.method == "POST":
        if id == 0:
            form = EditUserForm(request.POST)
        else:
            user = User_Account.objects.get(pk=id)
            form = EditUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        return redirect('SDMS:superuser-users')

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_deleteuser(request, id):
    user_account = User_Account.objects.get(pk=id)
    user_account.visible = 'HIDE'
    user = User.objects.get(pk=user_account.user.id)
    user.is_active = False
    user.save()
    user_account.save()
    return redirect('SDMS:superuser-users')

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_newuser(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            msg = 'New user created!'
            role = request.POST.get('user-role')
            group = Group.objects.get(name=str(role))
            user.groups.add(group)
            fname = request.POST.get('first_name')
            mname = request.POST.get('middle_name')
            lname = request.POST.get('last_name')
            cnumber = request.POST.get('contact_number')
            eml_addrs = request.POST.get('email_address')
            ppic = request.FILES['profile_picture']
            User_Account.objects.create(
                user = user,
                first_name = fname,
                middle_name = mname,
                last_name = lname,
                contact_number = cnumber,
                email_address = eml_addrs,
                profile_pic = ppic
            )
            return redirect('SDMS:superuser-users')
        else:
            msg = 'Form is invalid'
    else:
        form = SignUpForm()
    context = {'screen_name' : "New User",
    'form' : form,
    'msg' : msg
    }
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, "mobile/superuser_newuser.html", context)
    else:
        return render(request, "superuser_newuser.html", context)

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_activitylog(request):
    log = Activity_Log.objects.all().order_by('activity_date')
    context = {'screen_name' : "Activity Log",
    'log' : log
    }
    return render(request, "superuser_activitylog.html", context)

@login_required(login_url="SDMS:login")
@allowed_users(allowed_roles=['Admin'])
def superuser_forgotpassword(request):
    msg = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            try:
                user = User.objects.get(username=username)
                user.set_password(password1)
                user.save()
                msg = 'Password reset successful.'
                return redirect('SDMS:superuser-users')
            except User.DoesNotExist:
                msg = 'User not found.'
                return redirect('SDMS:superuser-forgotpassword')
        else:
            msg = 'Passwords do not match. Please try again.'
            return redirect('SDMS:superuser-forgotpassword')

    context = {'screen_name' : "Reset Password",
    'msg' : msg
    }
    return render(request, "superuser_resetpassword.html", context)


#MANAGEMENT
@login_required(login_url="login")
@allowed_users(allowed_roles=['Management'])
def management_home(request):
    current_user = User_Account.objects.get(user=request.user.id)
    user_firstname = current_user.first_name.split(' ')[0]
    unpaid_count = 0
    active_count = 0
    base_rate = 0
    adjustment = 0
    trips = Trips.objects.all()
    unpaid = Trips.objects.filter(payment_status="UNPAID")
    trips_today = Trips.objects.filter(trip_date=datetime.today())
    for i in unpaid:
        base_rate += (i.bag_count * i.farm.rate_code)
        adjustment += i.rate_adjustment
    for t in trips:
        if t.trip_status == "SCHEDULED":
            active_count += 1
        if t.trip_status == "IN PROGRESS":
            active_count += 1
        if t.payment_status == "UNPAID":
            unpaid_count += 1
    context = {'screen_name' : "Home",
    'first_name' : user_firstname,
    'unpaid_trips' : unpaid_count,
    'active_trips' : active_count,
    'receivables' : (base_rate + adjustment),
    'trips_today' : trips_today
    }
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, "mobile/management_home.html", context)
    else:
        return render(request, "management_home.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['Management'])
def management_trips(request):
    current_user = User_Account.objects.get(user=request.user.id)
    user_firstname = current_user.first_name.split(' ')[0]
    trips = Trips.objects.all().order_by('trip_date')

    context = {'screen_name' : "Trips",
    'first_name' : user_firstname,
    'trips' : trips
    }
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, "mobile/management_trips.html", context)
    else:
        return render(request, "management_trips.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['Management'])
def management_viewtrip(request, id):
    current_user = User_Account.objects.get(user=request.user.id)
    user_firstname = current_user.first_name.split(' ')[0]
    bag_over_cap = 0
    ref_no = None
    current_adjustment = 0
    if request.method == "GET":
        if id == 0:
            form = EditTrip_management()
        else:
            trip = Trips.objects.get(pk=id)
            form = EditTrip_management(instance=trip)
            ref_no = trip.ref_num
            truck_cap = trip.truck.capacity
            bag_count = trip.bag_count
            current_adjustment += trip.rate_adjustment
            check = bag_count - truck_cap
            if check > 0:
                bag_over_cap += abs(check)
            if check <= 0:
                bag_over_cap += 0
        context = {'form' : form,
            'first_name' : user_firstname,
            'screen_name' : ref_no,
            'trip' : trip,
            'bag_over_cap' : bag_over_cap}
        if request.user_agent.is_mobile or request.user_agent.is_tablet:
            return render(request, "mobile/management_viewtrip.html", context)
        else:
            return render(request, "management_viewtrip.html", context)
    if request.method == "POST":
        if id == 0:
            form = EditTrip_management(request.POST)
        else:
            trip = Trips.objects.get(pk=id)
            form = EditTrip_management(request.POST, request.FILES, instance=trip)
        if form.is_valid():
            form.save()
            current_datetime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            trip.last_edit_date = current_datetime
            trip.last_edit_by = User_Account.objects.get(user=request.user)
            trip.save()
            trip_month = trip.trip_date.month
            trip_year = trip.trip_date.year
            client_findata = Client_FinancialReport.objects.get(client__id=trip.farm.company.id, trip_month=trip_month, trip_year=trip_year)
            if current_adjustment != trip.rate_adjustment:
                if current_adjustment > trip.rate_adjustment:
                    current_adjustment -= trip.rate_adjustment
                    client_findata.rate_adjust = current_adjustment
                if current_adjustment < trip.rate_adjustment:
                    current_adjustment += trip.rate_adjustment
                    client_findata.rate_adjust = current_adjustment
                client_findata.save()
            Activity_Log.objects.create(
                user = User_Account.objects.get(user=request.user),
                action = 'ADJUSTMENT (' + trip.ref_num + ")"
            )
        return redirect('SDMS:management-trips')

@login_required(login_url="login")
@allowed_users(allowed_roles=['Management'])
def management_financialreport(request):  
    current_user = User_Account.objects.get(user=request.user.id)
    user_firstname = current_user.first_name.split(' ')[0]
    total_trips = 0
    active_trips = 0
    completed_trips = 0
    total_bags = 0
    active_bags = 0
    completed_bags = 0
    total_receivables = 0
    current_date = datetime.now()
    get_totals = Trips.objects.filter(trip_date__month=current_date.month, trip_date__year = current_date.year)
    for i in get_totals:
        total_trips += 1
        total_bags += i.bag_count
        if i.trip_status == 'SCHEDULED' or i.trip_status =='IN PROGRESS':
            active_trips += 1
            active_bags += i.bag_count
        if i.trip_status == 'DELIVERED':
            completed_trips += 1
            completed_bags += i.bag_count
        if i.payment_status == 'UNPAID':
            total_receivables += (i.base_rate + i.rate_adjustment)
    client_data = Client_FinancialReport.objects.filter(trip_month=int(current_date.month), trip_year=int(current_date.year)).order_by('client__id')
    driver_data = Driver_FinancialReport.objects.filter(trip_month=int(current_date.month), trip_year=int(current_date.year)).order_by('driver__id')
    context = {'screen_name' : "Financial Report",
    'first_name' : user_firstname,
    'total_trips' : total_trips,
    'active_trips' : active_trips,
    'completed_trips' : completed_trips,
    'total_bags' : total_bags,
    'active_bags' : active_bags,
    'completed_bags' : completed_bags,
    'total_receivables' : total_receivables,
    'client_data' : client_data,
    'driver_data' : driver_data,
    'month' : current_date.strftime("%b"),
    'year' : current_date.year
    }
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, "mobile/management_financial.html", context)
    else:
        return render(request, "management_financial.html", context)


#STAFF
@login_required(login_url="login")
@allowed_users(allowed_roles=['Staff'])
def staff_home(request):
    current_user = User_Account.objects.get(user=request.user.id)
    user_firstname = current_user.first_name.split(' ')[0]
    unpaid_count = 0
    active_count = 0
    base_rate = 0
    adjustment = 0
    trips = Trips.objects.all()
    unpaid = Trips.objects.filter(payment_status="UNPAID")
    trips_today = Trips.objects.filter(trip_date=datetime.today())
    for i in unpaid:
        base_rate += (i.base_rate + i.rate_adjustment)
        adjustment += i.rate_adjustment
    for t in trips:
        if t.trip_status == "SCHEDULED":
            active_count += 1
        if t.trip_status == "IN PROGRESS":
            active_count += 1
        if t.payment_status == "UNPAID":
            unpaid_count += 1
    context = {'screen_name' : "Home",
    'first_name' : user_firstname,
    'unpaid_trips' : unpaid_count,
    'active_trips' : active_count,
    'receivables' : (base_rate - adjustment),
    'trips_today' : trips_today
    }
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, "mobile/staff_home.html", context)
    else:
        return render(request, "staff_home.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['Staff'])
def staff_trips(request):
    current_user = User_Account.objects.get(user=request.user.id)
    user_firstname = current_user.first_name.split(' ')[0]
    all_trips = Trips.objects.all().order_by('trip_date')

    context = {'screen_name' : "Trips",
    'first_name' : user_firstname,
    'trips' : all_trips
    }
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, "mobile/staff_trips.html", context)
    else:
        return render(request, "staff_trips.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['Staff'])
def staff_newtrip(request, id=0):
    current_user = User_Account.objects.get(user=request.user.id)
    user_firstname = current_user.first_name.split(' ')[0]
    #current_time = None
    if request.method == "GET":
        if id == 0:
            form = NewTrip()
            #current_time = datetime.now()
        else:
            trip = Trips.objects.get(pk=id)
            form = NewTrip(instance=trip)
        context = {'form' : form,
            'first_name' : user_firstname,
            'screen_name' : 'New Trip',
        }
        if request.user_agent.is_mobile or request.user_agent.is_tablet:
            return render(request, "mobile/staff_newtrip.html", context)
        else:
            return render(request, "staff_newtrip.html", context)
    if request.method == "POST":
        if id == 0:
            form = NewTrip(request.POST)
        else:
            trip = Trips.objects.get(pk=id)
            form = NewTrip(request.POST, request.FILES, instance=trip)
        state = 0
        if form.is_valid():
            form.save()
            state += 1

            if state == 1:
                reference_no = generate_refno()

                get_farm_form = request.POST.get('farm')
                get_truck_form = request.POST.get('truck')

                farm_data = Farm.objects.get(id=get_farm_form)
                truck_data = Truck.objects.get(id=get_truck_form)

                distance_class = 0
                driver_basic = 0
                helper1_basic = 0
                helper2_basic = 0
                helper3_basic = 0

                if 0 <= farm_data.distance <= 40:
                    distance_class += 1
                if 41 <= farm_data.distance <= 80:
                    distance_class += 2
                if 81 <= farm_data.distance <= 120:
                    distance_class += 3
                if 121 <= farm_data.distance <= 160:
                    distance_class += 4
                if 161 <= farm_data.distance <= 200:
                    distance_class += 5
                if 201 <= farm_data.distance <= 240:
                    distance_class += 6
                if farm_data.distance == 310:
                    distance_class += 430
                if farm_data.distance == 340:
                    distance_class += 675

                if distance_class == 1 and truck_data.truck_classification == 'ELF':
                    driver_basic += 280
                    
                    helper1_basic += 180
                
                    helper2_basic += 180
                
                    helper3_basic += 180
                if distance_class == 1 and truck_data.truck_classification == 'FWD':
                    driver_basic += 330
                    
                    helper1_basic += 250
                
                    helper2_basic += 250
                
                    helper3_basic += 250
                if distance_class == 1 and truck_data.truck_classification == 'PFWD-1':
                    driver_basic += 430
                    
                    helper1_basic += 330
                
                    helper2_basic += 330
                
                    helper3_basic += 330
                if distance_class == 1 and truck_data.truck_classification == 'PFWD-2':
                    driver_basic += 530
                    
                    helper1_basic += 280
                
                    helper2_basic += 280
                
                    helper3_basic += 280
                
                if distance_class == 2 and truck_data.truck_classification == 'ELF':
                    driver_basic += 330
                    
                    helper1_basic += 180
                
                    helper2_basic += 180
                
                    helper3_basic += 180
                if distance_class == 2 and truck_data.truck_classification == 'FWD':
                    driver_basic += 430
                    
                    helper1_basic += 250
                
                    helper2_basic += 250
                
                    helper3_basic += 250
                if distance_class == 2 and truck_data.truck_classification == 'PFWD-1':
                    driver_basic += 580
                    
                    helper1_basic += 330
                
                    helper2_basic += 330
                
                    helper3_basic += 330
                if distance_class == 2 and truck_data.truck_classification == 'PFWD-2':
                    driver_basic += 730
                    
                    helper1_basic += 280
                
                    helper2_basic += 280
                
                    helper3_basic += 280
                
                if distance_class == 3 and truck_data.truck_classification == 'ELF':
                    driver_basic += 380
                    
                    helper1_basic += 200
                
                    helper2_basic += 200
                
                    helper3_basic += 200
                if distance_class == 3 and truck_data.truck_classification == 'FWD':
                    driver_basic += 500
                    
                    helper1_basic += 280
                
                    helper2_basic += 280
                
                    helper3_basic += 280 
                if distance_class == 3 and truck_data.truck_classification == 'PFWD-1':
                    driver_basic += 675
                    
                    helper1_basic += 380
                
                    helper2_basic += 380
                
                    helper3_basic += 380
                if distance_class == 3 and truck_data.truck_classification == 'PFWD-2':
                    driver_basic += 850
                    
                    helper1_basic += 320
                
                    helper2_basic += 320
                
                    helper3_basic += 320

                if distance_class == 4 and truck_data.truck_classification == 'ELF':
                    driver_basic += 430
                    
                    helper1_basic += 200
                
                    helper2_basic += 200
                
                    helper3_basic += 200
                if distance_class == 4 and truck_data.truck_classification == 'FWD':
                    driver_basic += 550
                    
                    helper1_basic += 280
                
                    helper2_basic += 280
                
                    helper3_basic += 280 
                
                '''
                if distance_class == 4 and truck_data.truck_classification == 'PFWD-1':
                    driver_basic += 675
                    
                    helper1_basic += 380
                
                    helper2_basic += 380
                
                    helper3_basic += 380
                if distance_class == 4 and truck_data.truck_classification == 'PFWD-2':
                    driver_basic += 850
                    
                    helper1_basic += 320
                
                    helper2_basic += 320
                
                    helper3_basic += 320
                '''

                if distance_class == 5 and truck_data.truck_classification == 'ELF':
                    driver_basic += 480
                    
                    helper1_basic += 215
                
                    helper2_basic += 215
                
                    helper3_basic += 215
                if distance_class == 5 and truck_data.truck_classification == 'FWD':
                    driver_basic += 600
                    
                    helper1_basic += 310
                
                    helper2_basic += 310
                
                    helper3_basic += 310

                if distance_class == 6 and truck_data.truck_classification == 'ELF':
                    driver_basic += 530
                    
                    helper1_basic += 215
                
                    helper2_basic += 215
                
                    helper3_basic += 215
                if distance_class == 6 and truck_data.truck_classification == 'FWD':
                    driver_basic += 650
                    
                    helper1_basic += 310
                
                    helper2_basic += 310
                
                    helper3_basic += 310

                trip = Trips.objects.all().last()
                get_truck = Truck.objects.get(id=trip.truck.id)
                capacity = get_truck.capacity
                trip.ref_num = reference_no
                #trip.start_time = start
                trip.driver_basic = driver_basic
                trip.helper1_basic = helper1_basic
                trip.helper2_basic = helper2_basic
                trip.helper3_basic = helper3_basic
                trip.create_by = request.user
                if trip.bag_count < (capacity * 0.70):
                    trip.base_rate += (Decimal(capacity * 0.70) * trip.farm.rate_code)
                else:
                    trip.base_rate += (trip.bag_count * trip.farm.rate_code)
                trip.save()
                current_date = datetime.today()
                try:
                    driver_findata = Driver_FinancialReport.objects.get(driver__id=trip.truck.driver.id, trip_month=current_date.month, trip_year=current_date.year)
                    driver_findata.trip_count += 1
                    driver_findata.bag_count += trip.bag_count
                    driver_findata.driver_basic += trip.driver_basic
                    driver_findata.save()
                except Driver_FinancialReport.DoesNotExist :
                    Driver_FinancialReport.objects.create(
                        driver = User_Account.objects.get(id=trip.truck.driver.id),
                        trip_month = int(current_date.month),
                        trip_year = int(current_date.year),
                        trip_count = 1,
                        bag_count = trip.bag_count,
                        driver_basic = trip.driver_basic
                    )
                try:
                    client_findata = Client_FinancialReport.objects.get(client__id=trip.farm.company.id, trip_month=current_date.month, trip_year=current_date.year)
                    client_findata.trip_inprogress += 1
                    client_findata.bag_count += trip.bag_count
                    if trip.bag_count < (capacity * 0.70):
                        client_findata.base_rate += ((Decimal(capacity * 0.70) * trip.farm.rate_code))
                    else:
                        client_findata.base_rate += (trip.bag_count * trip.farm.rate_code)
                    client_findata.save()
                except Client_FinancialReport.DoesNotExist:
                    base = 0
                    if trip.bag_count < (capacity * 0.70):
                        base += ((Decimal(capacity * 0.70) * trip.farm.rate_code))
                    else:
                        base += (trip.bag_count * trip.farm.rate_code)
                    Client_FinancialReport.objects.create(
                        client = Company.objects.get(id=trip.farm.company.id),
                        trip_month = int(current_date.month),
                        trip_year = int(current_date.year),
                        trip_inprogress = 1,
                        bag_count = trip.bag_count,
                        base_rate = base
                    )

                Activity_Log.objects.create(
                    user = User_Account.objects.get(user=request.user),
                    action = 'CREATE (' + reference_no + ")"
                )
            
        return redirect('SDMS:staff-trips')

@login_required(login_url="login")
@allowed_users(allowed_roles=['Staff'])
def staff_edittrip(request, id=0):
    current_user = User_Account.objects.get(user=request.user.id)
    user_firstname = current_user.first_name.split(' ')[0]
    ref_no = None
    bag_over_cap = 0
    current_tripstat = None
    current_paymentstat = None
    current_drivadd = 0
    if request.method == "GET":
        if id == 0:
            form = EditTrip_staff()
        else:
            trip = Trips.objects.get(pk=id)
            form = EditTrip_staff(instance=trip)
            ref_no = trip.ref_num
            truck_cap = trip.truck.capacity
            bag_count = trip.bag_count
            check = bag_count - truck_cap
            current_tripstat = trip.trip_status
            current_paymentstat = trip.payment_status
            current_drivadd += trip.driver_additional
            if check > 0:
                bag_over_cap += abs(check)
            if check <= 0:
                bag_over_cap += 0
        context = {'form' : form,
            'first_name' : user_firstname,
            'screen_name' : ref_no,
            'trip' : trip,
            'excess' : bag_over_cap,
            'trip_status' : current_tripstat,
            'payment_status' : current_paymentstat
            }
        if request.user_agent.is_mobile or request.user_agent.is_tablet:
            return render(request, "mobile/staff_edittrip.html", context)
        else:
            return render(request, "staff_edittrip.html", context)
    if request.method == "POST":
        if id == 0:
            form = EditTrip_staff(request.POST)
        else:
            trip = Trips.objects.get(pk=id)
            form = EditTrip_staff(request.POST, request.FILES, instance=trip)
        if form.is_valid():
            form.save()
            current_datetime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            trip.last_edit_date = current_datetime
            trip.last_edit_by = User_Account.objects.get(user=request.user)
            trip.save()
            trip_month = trip.trip_date.month
            trip_year = trip.trip_date.year
            client_findata = Client_FinancialReport.objects.get(client__id=trip.farm.company.id, trip_month=trip_month, trip_year=trip_year)
            if current_tripstat != trip.trip_status:
                client_findata.trip_inprogress -= 1
                client_findata.trip_completed += 1
                client_findata.save()
            if current_paymentstat != trip.payment_status:
                client_findata.base_rate -= (trip.bag_count * trip.farm.rate_code)
                client_findata.rate_adjust -= trip.rate_adjustment
                client_findata.save()
            if current_drivadd != trip.driver_additional:
                if current_drivadd > trip.driver_additional:
                    current_drivadd -= trip.driver_additional
                    client_findata.driver_additional = current_drivadd
                if current_drivadd < trip.driver_additional:
                    current_drivadd += trip.driver_additional
                    client_findata.driver_additional = current_drivadd
                client_findata.save()
            Activity_Log.objects.create(
                user = User_Account.objects.get(user=request.user),
                action = 'EDIT (' + trip.ref_num + ")"
            )
        return redirect('SDMS:staff-trips')

@login_required(login_url="login")
@allowed_users(allowed_roles=['Staff'])
def staff_financialreport(request):
    current_user = User_Account.objects.get(user=request.user.id)
    user_firstname = current_user.first_name.split(' ')[0]
    total_trips = 0
    active_trips = 0
    completed_trips = 0
    total_bags = 0
    active_bags = 0
    completed_bags = 0
    total_receivables = 0
    current_date = datetime.now()
    get_totals = Trips.objects.filter(trip_date__month=current_date.month, trip_date__year=current_date.year)
    for i in get_totals:
        total_trips += 1
        total_bags += i.bag_count
        if i.trip_status == 'SCHEDULED' or i.trip_status =='IN PROGRESS':
            active_trips += 1
            active_bags += i.bag_count
        if i.trip_status == 'DELIVERED':
            completed_trips += 1
            completed_bags += i.bag_count
        if i.payment_status == 'UNPAID':
            total_receivables += (i.base_rate + i.rate_adjustment)
    clients = Company.objects.all()
    get_users = User.objects.filter(groups__name__in=['Driver'])
    client_data = Client_FinancialReport.objects.filter(trip_month=int(current_date.month), trip_year=int(current_date.year)).order_by('client__id')
    driver_data = Driver_FinancialReport.objects.filter(trip_month=int(current_date.month), trip_year=int(current_date.year)).order_by('driver__id')

    context = {'screen_name' : "Financial Report",
    'first_name' : user_firstname,
    'clients' : clients,
    'total_trips' : total_trips,
    'active_trips' : active_trips,
    'completed_trips' : completed_trips,
    'total_bags' : total_bags,
    'active_bags' : active_bags,
    'completed_bags' : completed_bags,
    'total_receivables' : total_receivables,
    'users' : get_users,
    'client_data' : client_data,
    'driver_data' : driver_data,
    'month' : str(current_date.strftime("%b")),
    'year' : str(current_date.year)
    }
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, "mobile/staff_financial.html", context)
    else:
        return render(request, "staff_financial.html", context)

#DRIVER
@login_required(login_url="login")
@allowed_users(allowed_roles=['Driver'])
def driver_home(request):
    current_user = User_Account.objects.get(user=request.user.id)
    user_firstname = current_user.first_name.split(' ')[0]
    active_count = 0
    completed_count_mobile = 0
    active_count_mobile = 0
    bag_total = 0
    current_week = date.today().isocalendar()[1]
    driver_active_trips = Trips.objects.filter(Q(truck__driver__user=request.user.id, trip_status="IN PROGRESS")|Q(truck__driver__user=request.user.id, trip_status="SCHEDULED")).order_by('trip_date')
    for trip in driver_active_trips:
        if trip.trip_status == "IN PROGRESS" or trip.trip_status == "SCHEDULED":
            active_count +=1
    entries = Trips.objects.filter(truck__driver__user=request.user.id, trip_date__week=current_week)
    for bag in entries:
        bag_total += bag.bag_count
        if trip.trip_status == "IN PROGRESS" or trip.trip_status == "SCHEDULED":
            active_count_mobile +=1
        if bag.trip_status == 'DELIVERED':
            completed_count_mobile += 1
    context = {'screen_name' : "Home",
    'first_name' : user_firstname,
    'active_trips' : active_count,
    'bag_total' : bag_total,
    'trips' : driver_active_trips,
    'active_mobile' : active_count_mobile,
    'completed_mobile' : completed_count_mobile
    }
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, "mobile/driver_home.html", context)
    else:
        return render(request, "driver_home.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['Driver'])
def driver_trips(request):
    current_user = User_Account.objects.get(user=request.user.id)
    user_firstname = current_user.first_name.split(' ')[0]
    driver_active_trips = Trips.objects.filter(Q(truck__driver__user=request.user.id, trip_status="IN PROGRESS")|Q(truck__driver__user=request.user.id, trip_status="SCHEDULED")).order_by('trip_date')
    context = {'screen_name' : "Trips",
    'first_name' : user_firstname,
    'trips' : driver_active_trips
    }
    return render(request, "mobile/driver_trips.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['Driver'])
def driver_newtrip(request, id=0):
    current_user = User_Account.objects.get(user=request.user.id)
    user_firstname = current_user.first_name.split(' ')[0]
    current_time = None
    if request.method == "GET":
        if id == 0:
            form = NewTrip_driver()
            current_time = datetime.now()
        else:
            trip = Trips.objects.get(pk=id)
            form = NewTrip_driver(instance=trip)
        context = {'form' : form,
            'first_name' : user_firstname,
            'screen_name' : 'New Trip',
        }
        if request.user_agent.is_mobile or request.user_agent.is_tablet:
            return render(request, "mobile/driver_newtrip.html", context)
        else:
            return render(request, "driver_newtrip.html", context)
    if request.method == "POST":
        if id == 0:
            form = NewTrip_driver(request.POST)
        else:
            trip = Trips.objects.get(pk=id)
            form = NewTrip_driver(request.POST, request.FILES, instance=trip)
        state = 0
        if form.is_valid():
            form.save()
            state += 1
            if state == 1:
                reference_no = generate_refno()
                get_farm_form = request.POST.get('farm')
                farm_data = Farm.objects.get(id=get_farm_form)
                get_current_driver = User_Account.objects.get(user__id=request.user.id)
                truck_data = Truck.objects.get(driver=get_current_driver)
                distance_class = 0
                driver_basic = 0
                helper1_basic = 0
                helper2_basic = 0
                helper3_basic = 0
                if 0 <= farm_data.distance <= 40:
                    distance_class += 1
                if 41 <= farm_data.distance <= 80:
                    distance_class += 2
                if 81 <= farm_data.distance <= 120:
                    distance_class += 3
                if 121 <= farm_data.distance <= 160:
                    distance_class += 4
                if 161 <= farm_data.distance <= 200:
                    distance_class += 5
                if 201 <= farm_data.distance <= 240:
                    distance_class += 6
                if farm_data.distance == 310:
                    distance_class += 430
                if farm_data.distance == 340:
                    distance_class += 675

                if distance_class == 1 and truck_data.truck_classification == 'ELF':
                    driver_basic += 280
                    helper1_basic += 180
                    helper2_basic += 180
                    helper3_basic += 180
                if distance_class == 1 and truck_data.truck_classification == 'FWD':
                    driver_basic += 330
                    helper1_basic += 250
                    helper2_basic += 250
                    helper3_basic += 250
                if distance_class == 1 and truck_data.truck_classification == 'PFWD-1':
                    driver_basic += 430
                    helper1_basic += 330
                    helper2_basic += 330
                    helper3_basic += 330
                if distance_class == 1 and truck_data.truck_classification == 'PFWD-2':
                    driver_basic += 530
                    
                    helper1_basic += 280
                
                    helper2_basic += 280
                
                    helper3_basic += 280
                
                if distance_class == 2 and truck_data.truck_classification == 'ELF':
                    driver_basic += 330
                    
                    helper1_basic += 180
                
                    helper2_basic += 180
                
                    helper3_basic += 180
                if distance_class == 2 and truck_data.truck_classification == 'FWD':
                    driver_basic += 430
                    
                    helper1_basic += 250
                
                    helper2_basic += 250
                
                    helper3_basic += 250
                if distance_class == 2 and truck_data.truck_classification == 'PFWD-1':
                    driver_basic += 580
                    
                    helper1_basic += 330
                
                    helper2_basic += 330
                
                    helper3_basic += 330
                if distance_class == 2 and truck_data.truck_classification == 'PFWD-2':
                    driver_basic += 730
                    
                    helper1_basic += 280
                
                    helper2_basic += 280
                
                    helper3_basic += 280
                
                if distance_class == 3 and truck_data.truck_classification == 'ELF':
                    driver_basic += 380
                    
                    helper1_basic += 200
                
                    helper2_basic += 200
                
                    helper3_basic += 200
                if distance_class == 3 and truck_data.truck_classification == 'FWD':
                    driver_basic += 500
                    
                    helper1_basic += 280
                
                    helper2_basic += 280
                
                    helper3_basic += 280 
                if distance_class == 3 and truck_data.truck_classification == 'PFWD-1':
                    driver_basic += 675
                    
                    helper1_basic += 380
                
                    helper2_basic += 380
                
                    helper3_basic += 380
                if distance_class == 3 and truck_data.truck_classification == 'PFWD-2':
                    driver_basic += 850
                    
                    helper1_basic += 320
                
                    helper2_basic += 320
                
                    helper3_basic += 320

                if distance_class == 4 and truck_data.truck_classification == 'ELF':
                    driver_basic += 430
                    
                    helper1_basic += 200
                
                    helper2_basic += 200
                
                    helper3_basic += 200
                if distance_class == 4 and truck_data.truck_classification == 'FWD':
                    driver_basic += 550
                    
                    helper1_basic += 280
                
                    helper2_basic += 280
                
                    helper3_basic += 280 
                
                '''
                if distance_class == 4 and truck_data.truck_classification == 'PFWD-1':
                    driver_basic += 675
                    
                    helper1_basic += 380
                
                    helper2_basic += 380
                
                    helper3_basic += 380
                if distance_class == 4 and truck_data.truck_classification == 'PFWD-2':
                    driver_basic += 850
                    
                    helper1_basic += 320
                
                    helper2_basic += 320
                
                    helper3_basic += 320
                '''

                if distance_class == 5 and truck_data.truck_classification == 'ELF':
                    driver_basic += 480
                    
                    helper1_basic += 215
                
                    helper2_basic += 215
                
                    helper3_basic += 215
                if distance_class == 5 and truck_data.truck_classification == 'FWD':
                    driver_basic += 600
                    
                    helper1_basic += 310
                
                    helper2_basic += 310
                
                    helper3_basic += 310

                if distance_class == 6 and truck_data.truck_classification == 'ELF':
                    driver_basic += 530
                    
                    helper1_basic += 215
                
                    helper2_basic += 215
                
                    helper3_basic += 215
                if distance_class == 6 and truck_data.truck_classification == 'FWD':
                    driver_basic += 650
                    
                    helper1_basic += 310
                
                    helper2_basic += 310
                
                    helper3_basic += 310
                trip = Trips.objects.all().last()
                trip.ref_num = reference_no
                get_truck = Truck.objects.get(driver__user=request.user.id)
                capacity = get_truck.capacity
                get_current_driver = User_Account.objects.get(user__id=request.user.id)
                trip.truck = Truck.objects.get(driver=get_current_driver)
                trip.driver_basic = driver_basic
                trip.start_time = current_time
                trip.helper1_basic = helper1_basic
                trip.helper2_basic = helper2_basic
                trip.helper3_basic = helper3_basic
                trip.create_by = request.user
                if trip.bag_count < (capacity * 0.70):
                    trip.base_rate += (Decimal(capacity * 0.70) * trip.farm.rate_code)
                else:
                    trip.base_rate += (trip.bag_count * trip.farm.rate_code)
                trip.save()
                current_date = datetime.today()
                try:
                    driver_findata = Driver_FinancialReport.objects.get(driver__id=trip.truck.driver.id, trip_month=current_date.month, trip_year=current_date.year)
                    driver_findata.trip_count += 1
                    driver_findata.bag_count += trip.bag_count
                    driver_findata.driver_basic += trip.driver_basic
                    driver_findata.save()
                except Driver_FinancialReport.DoesNotExist :
                    Driver_FinancialReport.objects.create(
                        driver = User_Account.objects.get(id=trip.truck.driver.id),
                        trip_month = int(current_date.month),
                        trip_year = int(current_date.year),
                        trip_count = 1,
                        bag_count = trip.bag_count,
                        driver_basic = trip.driver_basic
                    )
                try:
                    client_findata = Client_FinancialReport.objects.get(client__id=trip.farm.company.id, trip_month=current_date.month, trip_year=current_date.year)
                    client_findata.trip_inprogress += 1
                    client_findata.bag_count += trip.bag_count
                    if trip.bag_count < (capacity * 0.70):
                        client_findata.base_rate += (Decimal(capacity * 0.70) * trip.farm.rate_code)
                    else:
                        client_findata.base_rate += (trip.bag_count * trip.farm.rate_code)
                    client_findata.save()
                except Client_FinancialReport.DoesNotExist:
                    base = 0
                    if trip.bag_count < (capacity * 0.70):
                        base += (Decimal(capacity * 0.70) * trip.farm.rate_code)
                    else:
                        base += (trip.bag_count * trip.farm.rate_code)
                    Client_FinancialReport.objects.create(
                        client = Company.objects.get(id=trip.farm.company.id),
                        trip_month = int(current_date.month),
                        trip_year = int(current_date.year),
                        trip_inprogress = 1,
                        bag_count = trip.bag_count,
                        base_rate = base
                    )
                Activity_Log.objects.create(
                    user = User_Account.objects.get(user=request.user),
                    action = 'CREATE (' + reference_no + ")"
                )
        if request.user_agent.is_mobile or request.user_agent.is_tablet:
            return redirect('SDMS:driver-trips')
        else:  
            return redirect('SDMS:driver-home')

@login_required(login_url="login")
@allowed_users(allowed_roles=['Driver'])
def driver_edittrip(request, id=0):
    current_user = User_Account.objects.get(user=request.user.id)
    user_firstname = current_user.first_name.split(' ')[0]
    ref_no = None
    bag_over_cap = 0
    current_tripstat = None
    if request.method == "GET":
        if id == 0:
            form = EditTrip_driver()
        else:
            trip = Trips.objects.get(pk=id)
            form = EditTrip_driver(instance=trip)
            ref_no = trip.ref_num
            truck_cap = trip.truck.capacity
            bag_count = trip.bag_count
            current_tripstat = trip.trip_status
            check = bag_count - truck_cap
            if check > 0:
                bag_over_cap += abs(check)
            if check <= 0:
                bag_over_cap += 0
        context = {'form' : form,
            'first_name' : user_firstname,
            'screen_name' : ref_no,
            'trip' : trip,
            'excess' : bag_over_cap,
            'trip_status' : current_tripstat    
        }
        if request.user_agent.is_mobile or request.user_agent.is_tablet:
            return render(request, "mobile/driver_edittrip.html", context)
        else:
            return render(request, "driver_edittrip.html", context)

    if request.method == "POST":
        if id == 0:
            form = EditTrip_driver(request.POST)
        else:
            trip = Trips.objects.get(pk=id)
            form = EditTrip_driver(request.POST, request.FILES, instance=trip)
        if form.is_valid():
            form.save()
            current_datetime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            trip.last_edit_date = current_datetime
            trip.last_edit_by = User_Account.objects.get(user=request.user)
            trip.save()
            trip_month = trip.trip_date.month
            trip_year = trip.trip_date.year
            client_findata = Client_FinancialReport.objects.get(client__id=trip.farm.company.id, trip_month=trip_month, trip_year=trip_year)
            if current_tripstat != trip.trip_status:
                client_findata.trip_inprogress -= 1
                client_findata.trip_completed += 1
                client_findata.save()
            Activity_Log.objects.create(
                user = User_Account.objects.get(user=request.user),
                action = 'EDIT (' + trip.ref_num + ")"
            )
        return redirect('SDMS:driver-home')