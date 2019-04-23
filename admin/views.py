from django.shortcuts import render, redirect
from users.models import Profile, Record, Appointment, File
from django.contrib.auth.models import User
from django.utils.timezone import now
from .forms import RequestDocumentForm, AppointmentForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

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
        if request.method != "POST":
                form = RequestDocumentForm()
        else :
                form = RequestDocumentForm(request.POST) 
                
                if form.is_valid():
                        desc = form.cleaned_data.get('description') 
                        send_mail(
                        'Requested Documents From Dr. Serhal',
                        f'{desc}',
                        settings.EMAIL_HOST_USER,
                        [user.email,]
                        )
                        messages.success(request,f'An email was successfully sent to {user.first_name} requesting a {desc}')        
                else :
                        messages.error(request,'Please enter a valid description!')
        profile = Profile.objects.get(user=user)
        record = Record.objects.get(user=user)
        user_apps = Appointment.objects.filter(user=user, date__gte=now())
        user_passed_apps = Appointment.objects.filter(user=user, date__lte=now())
        user_files =  File.objects.filter(user=user)
        context = {
                'requested_user':user,
                'profile':profile,
                'record':record,
                'upcoming_appointments':user_apps,
                'previous_appointments':user_passed_apps,
                'files': user_files,
                'form': form
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

def add_appointments(request):
        if request.user.is_superuser:
                if request.method == 'POST':
                        form=AppointmentForm(request.POST)
                        if form.is_valid():
                                date = form.cleaned_data.get('date')
                                appointments=Appointment.objects.filter(date=date)
                                if any(appointments) or date < now() :
                                        messages.error(request,'Invalid Time.')
                                
                                else :
                                        user = User.objects.get(username=form.cleaned_data.get('users_field'))
                                        appointment=form.save(commit=False)
                                        appointment.user=user
                                        appointment.save()
                                        messages.success(request,f'You have successfully taken an appointment for {user.first_name}')
                                        send_mail(
                                                'Appointment With Dr. Serhal',
                                                f'You have successfully taken an appointment.\nDate: {appointment.date}.',
                                                settings.EMAIL_HOST_USER,
                                                [user.email,]
                                        )
                                        return redirect('add-appointments')
                                
                        else:
                                messages.error(request,'Please complete all info')
                else:
                        form=AppointmentForm()
                return render(request,'admin/add-appointments.html',{'form':form})
        else :
                return redirect('login')