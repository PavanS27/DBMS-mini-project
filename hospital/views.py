from django.shortcuts import render,redirect
from django.utils import timezone
from .models import *
from django.contrib.auth.models import User,Group
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse
def homepage(request):
    return render(request,'index.html')

def aboutpage(request):
    return render(request,'about.html')

def Login_admin(request):
	error = ""
	if request.method == 'POST':
		u = request.POST['username']
		p = request.POST['password']
		user = authenticate(username=u,password=p)
		try:
			if user.is_staff:
				login(request,user)
				error = "no"
			else:
				error = "yes"
		except:
			error = "yes"
	d = {'error' : error}
	return render(request,'adminlogin.html',d)

def Logout_admin(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	logout(request)
	return redirect('login_admin')

def AdminHome(request):
	#after login user comes to this page.
	if not request.user.is_staff:
		return redirect('login_admin')
	return render(request,'adminhome.html')

def adminaddDoctor(request):
	error = ""
	user="none"
	if not request.user.is_staff:
		return redirect('login_admin')

	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		password = request.POST['password']
		repeatpassword =  request.POST['repeatpasssword']
		gender = request.POST['gender']
		phonenumber = request.POST['phonenumber']
		address = request.POST['address']
		birthdate = request.POST['birthdate']
		bloodgroup = request.POST['bloodgroup']
		specialization = request.POST['specialization']
		
		try:
			if password == repeatpassword:
				Doctor.objects.create(name=name,email=email,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup,specialization=specialization)
				user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
				doc_group = Group.objects.get(name='Doctor')
				doc_group.user_set.add(user)
				user.save()
				error = "no"
			else:
				error = "yes"
		except Exception as e:
			error = "yes"
	d = {'error' : error}
	return render(request,'adminadddoctor.html',d)

def adminviewDoctor(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	doc = Doctor.objects.all()
	d = { 'doc' : doc }
	return render(request,'adminviewDoctors.html',d)



def admin_delete_doctor(request,pid,email):
	if not request.user.is_staff:
		return redirect('login_admin')
	doctor = Doctor.objects.get(id=pid)
	doctor.delete()
	users = User.objects.filter(username=email)
	users.delete()
	return redirect('adminviewDoctor')

def adminaddReceptionist(request):
	error = ""
	if not request.user.is_staff:
		return redirect('login_admin')

	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		password = request.POST['password']
		repeatpassword = request.POST['repeatpassword']
		gender = request.POST['gender']
		phonenumber = request.POST['phonenumber']
		address = request.POST['address']
		birthdate = request.POST['birthdate']
		bloodgroup = request.POST['bloodgroup']

		try:
			if password == repeatpassword:
				Receptionist.objects.create(name=name,email=email,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup)
				user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
				rec_group = Group.objects.get(name='Receptionist')
				rec_group.user_set.add(user)
				#print(rec_group)
				user.save()
				#print(user)
				error = "no"
			else:
				error = "yes"
		except:
			error = "yes"
	d = { 'error' : error }
	return render(request,'adminaddreceptionist.html',d)

def adminviewReceptionist(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	rec = Receptionist.objects.all()
	r = { 'rec' : rec }
	return render(request,'adminviewreceptionists.html',r)

def admin_delete_receptionist(request,pid,email):
	if not request.user.is_staff:
		return redirect('login_admin')
	reception = Receptionist.objects.get(id=pid)
	reception.delete()
	users = User.objects.filter(username=email)
	users.delete()
	return redirect('adminviewReceptionist')

def adminviewAppointment(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	upcomming_appointments = Appointment.objects.filter(appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')
	#print("Upcomming Appointment",upcomming_appointments)
	previous_appointments = Appointment.objects.filter(appointmentdate__lt=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(status=False).order_by('-appointmentdate')
	#print("Previous Appointment",previous_appointments)
	d = { "upcomming_appointments" : upcomming_appointments, "previous_appointments" : previous_appointments }
	return render(request,'adminviewappointments.html',d)

# def admin_delete_appointment(request,b_id):
#     appointment = Appointment.objects.get(id=b_id)
#     appointment.delete()
#     return redirect('adminviewAppointment')
def loginpage(request):
    error = ""
    if request.method == "POST":
        u = request.POST['email']
        p = request.POST['password']

        user = authenticate(request,username=u,password=p)
        try:
            if user is not None:
                error = "no"
                login(request,user)
                g =  request.user.groups.all()[0].name
                if g == 'Patient':
                    d = {'error':error}
                    return render(request,'patienthome.html',d)
                elif g == "Doctor":
                    d = {'error':error}
                    return render(request,'doctorhome.html',d)
                elif g == "Receptionist":
                    d = {'error':error}
                    return render(request,'receptionhome.html',d)
        except Exception as e:
            raise e

    return render(request,'login.html')
def signup(request):
    user = 'none'
    error = ''
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['birthdate']
        bloodgroup = request.POST['bloodgroup']

        try:
            if password == repeatpassword:
                Patient.objects.create(name=name,email=email,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup)
                user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
                pat_grp = Group.objects.get(name='Patient')
                pat_grp.user_set.add(user)
                user.save()
                error = 'no'
            else:
                error = 'yes'
        except Exception as e:
            #raise e
            error = 'yes' 
    d = {'error':error}
    return render(request,'createaccount.html',d)


def Logout(request):
    logout(request)
    return redirect('loginpage')

def Home(request):
    if not request.user.is_active:
        return redirect('loginpage')

    g = request.user.groups.all()[0].name
    print(g)
    if g == "Patient":
        return render(request,'patienthome.html')
    elif g == "Doctor":
        return render(request,'doctorhome.html')
    elif g == "Receptionist":
        return render(request,'receptionhome.html')

def profile(request):
    if not request.user.is_active:
        return redirect('loginpage')

    g = request.user.groups.all()[0].name
    if g == "Patient":
        patient_details = Patient.objects.all().filter(email=request.user)
        d = {'patient_details':patient_details}
        return render(request,'pateintprofile.html',d)
    if g == "Doctor":
        doctor_details = Doctor.objects.all().filter(email=request.user)
        print(list(doctor_details))
        d = {'doctor_details':doctor_details}
       
        return render(request,'doctorprofile.html',d)
    if g == "Receptionist":
        receptionist_details = Receptionist.objects.all().filter(email=request.user)
        d = {'receptionist_details':receptionist_details}
       
        return render(request,'receptionprofile.html',d)

def MakeAppointment(request):
    if not request.user.is_active:
        return redirect('loginpage')
    error = ""
    alldoctors = Doctor.objects.all()
    d = {'alldoctors':alldoctors}

    if request.method == "POST":
        temp = request.POST['doctoremail']
        doctoremail = temp.split()[0]
        doctorname = temp.split()[1]
        patientname = request.POST['patientname']
        patientemail = request.POST['patientemail']
        appointmentdate= request.POST['appointmentdate']
        appointmenttime = request.POST['appointmenttime']
        symptoms = request.POST['symptoms']
        try:
            Appointment.objects.create(doctorname=doctorname,doctoremail=doctoremail,patientname=patientname,patientemail=patientemail,appointmentdate=appointmentdate,appointmenttime=appointmenttime,symptoms=symptoms,status=True,prescription="")
            error = 'no'
        except Exception as e:
            error = 'yes'
        e =  {'error':error}
        return render(request,'pateintmakeappointments.html',e)
    return render(request,'pateintmakeappointments.html',d)


def viewappointment(request):
    if not request.user.is_active:
        return redirect('loginpage')

    g = request.user.groups.all()[0].name
    if g == 'Patient':
        upcoming_appointments = Appointment.objects.filter(patientemail=request.user,appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')
        previous_appointments = Appointment.objects.filter(patientemail=request.user,appointmentdate__lt=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(patientemail=request.user,status=False).order_by('-appointmentdate')
        d = {'upcoming_appointments':upcoming_appointments,'previous_appointments':previous_appointments}
        return render(request,'patientviewappointments.html',d)
    if g == 'Doctor':
        if request.method == "POST":
            prescriptiondata = request.POST['prescription']
            idvalue = request.POST['idofappointment']
            Appointment.objects.filter(id=idvalue).update(prescription=prescriptiondata,status=False)
        #upcoming_appointments = Appointment.objects.all()
        upcoming_appointments = Appointment.objects.filter(doctoremail=request.user,appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')
        previous_appointments = Appointment.objects.filter(doctoremail=request.user,appointmentdate__lt=timezone.now()).order_by('-appointmentdate')| Appointment.objects.filter(doctoremail=request.user,status=False).order_by('-appointmentdate')
        d = {'upcoming_appointments':upcoming_appointments,'previous_appointments':previous_appointments}
        return render(request,'doctorviewappointment.html',d)
    if g == 'Receptionist':
        upcoming_appointments = Appointment.objects.filter(appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')
        previous_appointments = Appointment.objects.filter(appointmentdate__lt=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(status=False).order_by('-appointmentdate')
        d = {'upcoming_appointments':upcoming_appointments,'previous_appointments':previous_appointments}
        return render(request,'receptionviewappointments.html',d)


def patient_view_pres(request):
    if not request.user.is_active:
        return redirect('loginpage')
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        pres = Appointment.objects.filter(patientemail=request.user)
        pat = Patient.objects.filter(email=request.user)
        d = {'pres':pres,'pat':pat}
    return render(request,'patientviewprescription.html',d)

def patient_delete_appointment(request,a_id):
    appointment = Appointment.objects.get(id=a_id)
    appointment.delete()
    return redirect('viewappointment')


        
