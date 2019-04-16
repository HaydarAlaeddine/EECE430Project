from django.shortcuts import render, redirect
from users.models import Profile, Record, Appointment
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your views here.
def view_patients(request):
    if request.user.is_superuser:
        patients = User.objects.filter(is_superuser=False)
        context = {'patients': patients,'number':len(patients)}
        return render(request,'admin/patients.html',context)
    else:
        return redirect(request,'user/login.html')

def get_patient(request,username):
    if request.user.is_superuser:    
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        record = Record.objects.get(user=user)
        user_apps = Appointment.objects.filter(user=user, date__gte=now())
        user_passed_apps = Appointment.objects.filter(user=user, date__lte=now()) 
        context = {
                'requested_user':user,
                'profile':profile,
                'record':record,
                'upcoming_appointments':user_apps,
                'previous_appointments':user_passed_apps
        }
        return render(request,'admin/patient-details.html',context)
    else:
        return redirect(request,'user/login.html')
def get_appointments(request):
        if request.user.is_superuser:    
                appointments = Appointment.objects.filter(date__gte=now())
                context= {
                        'appointments':appointments,
                        'number':len(appointments)
                }
                print(appointments)
                return render(request,'admin/appointments.html',context)
        else:
                return redirect(request,'user/login.html')


        
