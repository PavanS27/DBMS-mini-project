from django.contrib import admin
from django.urls import path
from hospital.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage,name="homepage"),
    path('about/', aboutpage,name="aboutpage"),
    path('loginpage/', loginpage,name="loginpage"),
    path('admin_login/',Login_admin,name='login_admin'),
    path('adminhome/',AdminHome,name='adminhome'),
    path('adminlogout/',Logout_admin,name='adminlogout'),
    path('adminaddDoctor/',adminaddDoctor,name='adminaddDoctor'),
    path('adminviewDoctor/',adminviewDoctor,name='adminviewDoctor'),
    path('adminDeleteDoctor<int:pid><str:email>',admin_delete_doctor,name='admin_delete_doctor'),
    path('adminaddReceptionist/',adminaddReceptionist,name='adminaddReceptionist'),
    path('adminviewReceptionist/',adminviewReceptionist,name='adminviewReceptionist'),
    path('adminDeleteReceptionist<int:pid>,<str:email>',admin_delete_receptionist,name='admin_delete_receptionist'),
    path('adminviewAppointment/',adminviewAppointment,name='adminviewAppointment'),
    # path('deleteappointment<int:b_id>', admin_delete_appointment,name="admin_delete_appointment"),
    path('signup/', signup,name="signup"),
    path('logout/', Logout,name="Logout"),
    path('pat_home/', Home,name="Home"),
    path('prescription/', patient_view_pres,name="patient_view_pres"),
    path('profile/', profile,name="profile"),
    path('makeappointments/', MakeAppointment,name="MakeAppointment"),
    path('viewappointments/', viewappointment,name="viewappointment"),
    path('deleteappointment<int:a_id>', patient_delete_appointment,name="patient_delete_appointment"),
   
]
