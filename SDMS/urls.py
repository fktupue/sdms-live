from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
app_name = 'SDMS'

urlpatterns = [
    #Login
    path('login/', views.login_user, name='login'),
    path('', lambda req: redirect('SDMS:login')),
    path('logout/', views.logout_user, name='logout'),

    #Superuser
    path('superuser-home/', views.superuser_home, name='superuser-home'),
    path('superuser-home/edit<str:id>', views.superuser_edittrip, name='superuser-edittrip'),
    path('superuser-home/delete<str:id>', views.superuser_deletetrip, name='superuser-deletetrip'),
    path('trip-search', csrf_exempt(views.search_trip), name='search-trip'),
    path('superuser-calendar', views.superuser_calendar, name='superuser-calendar'),
    path('superuser-clients', views.superuser_clientdata, name='superuser-clientdata'),
    path('client-search', csrf_exempt(views.search_client), name='search-client'),
    path('superuser-farms', views.superuser_farmdata, name='superuser-farmdata'),
    path('farm-search', csrf_exempt(views.search_farm), name='search-farm'),
    path('superuser-trucks', views.superuser_truckdata, name='superuser-truckdata'),
    path('truck-search', csrf_exempt(views.search_truck), name='search-truck'),
    path('superuser-newcompany', views.superuser_newcompany, name='superuser-newcompany'),
    path('superuser-company/cl<str:id>', views.superuser_newcompany, name='superuser-editcompany'),
    path('superuser-company/delete/cl<str:id>/', views.superuser_clientdelete, name="client-delete"),
    path('superuser-newfarm', views.superuser_newfarm, name='superuser-newfarm'),
    path('superuser-farms/frm<str:id>', views.superuser_newfarm, name='superuser-editfarm'),
    path('superuser-farms/delete/frm<str:id>/', views.superuser_farmdelete, name="farm-delete"),
    path('superuser-newtruck', views.superuser_newtruck, name='superuser-newtruck'),
    path('superuser-trucks/truck<str:id>', views.superuser_newtruck, name='superuser-edittruck'),
    path('superuser-trucks/delete/truck<str:id>/', views.superuser_truckdelete, name="truck-delete"),
    path('superuser-users', views.superuser_users, name='superuser-users'),
    path('user-search', csrf_exempt(views.search_user), name='search-user'),
    path('superuser-users/user<str:id>', views.superuser_edituser, name='edit-user'),
    path('superuser-users/delete/user<str:id>', views.superuser_deleteuser, name='delete-user'),
    path('superuser-newuser', views.superuser_newuser, name='superuser-newuser'),
    path('superuser-activitylog', views.superuser_activitylog, name='superuser-activitylog'),
    path('superuser-forgotpassword', views.superuser_forgotpassword, name='superuser-forgotpassword'),

    #calendar
    path('calendar', csrf_exempt(views.calendar), name='calendar'),

    #Management
    path('management-home/', views.management_home, name='management-home'),
    path('management-trips', views.management_trips, name='management-trips'),
    path('management-newtrip', views.management_newtrip, name='management-newtrip'),
    path('management-trips/trip<str:id>', views.management_viewtrip, name='management-viewtrip'),
    path('management-trips/generate-tripreport', views.generate_report, name='management-generatetripreport'),
    path('financialreport-download/cl<str:id>-<int:trip_month>-<int:trip_year>', views.generate_financialreport, name='management-generatefinancialreport'),
    path('management-financialreport', views.management_financialreport, name='management-financialreport'),
    path('totals-financial-data', csrf_exempt(views.totals_financial_report_data), name='totals-financial-data'),
    path('client-financial-data', csrf_exempt(views.client_financial_report_data), name='client-financial-data'),
    path('driver-financial-data', csrf_exempt(views.driver_financial_report_data), name='driver-financial-data'),
    

    #Staff
    path('staff-home/', views.staff_home, name='staff-home'),
    path('staff-trips', views.staff_trips, name='staff-trips'),
    path('staff-newtrip', views.staff_newtrip, name='staff-newtrip'),
    path('staff-trips/<str:id>', views.staff_edittrip, name='staff-viewtrip'),

    #Driver
    path('driver-home/', views.driver_home, name='driver-home'),
    path('driver-trip-search', csrf_exempt(views.driver_search_trip), name='driver-search-trip'),
    path('driver-trips', views.driver_trips, name='driver-trips'),
    path('driver-newtrip', views.driver_newtrip, name='driver-newtrip'),
    path('driver-trips/<str:id>', views.driver_edittrip, name='driver-viewtrip'),
]