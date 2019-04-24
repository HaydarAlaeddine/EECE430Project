from django.shortcuts import render, redirect
from users.models import Profile, Record, Appointment, File
from django.contrib.auth.models import User
from django.utils.timezone import now
from .forms import RequestDocumentForm, AppointmentForm,ModifyAppointmentForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse


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
                        pass
        profile = Profile.objects.get(user=user)
        record = Record.objects.get(user=user)
        user_apps = Appointment.objects.filter(user=user, date__gt=now())
        user_passed_apps = Appointment.objects.filter(user=user, date__lte=now(),missed=False)
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
                users = User.objects.filter(is_superuser=False)
                appointments = []
                for user in users:
                        user_apps = Appointment.objects.filter(user=user,date__gt=now()).order_by('date')
                        if any(user_apps):
                                appointments.append(user_apps[0])
                context= {
                        'appointments':appointments,
                        'number':len(appointments),
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
                                if date<now():
                                        messages.error(request,'This date is in the past!')
                                elif  any(appointments):
                                        messages.error(request,'Time Already Taken.')
                                else :
                                        user = User.objects.get(username=form.cleaned_data.get('users_field'))
                                        appointment=form.save(commit=False)
                                        appointment.user=user
                                        appointment.online=False
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

def delete_appointment(request,id):
        if request.user.is_superuser:
                appointment = Appointment.objects.get(id=id)
                appointment.delete()
                send_mail(
                        'Appointment With Dr. Serhal Deleted!',
                        f'Your appointment due on {appointment.date} with Dr. Serhal has been deleted.\nFor further contact us on 76784229.',
                        settings.EMAIL_HOST_USER,
                        [appointment.user.email,]
                )
                messages.success(request,'Appointment Successfully Deleted!')
                return get_patient(request,appointment.username)
        else:
                return redirect('login')

def modify_appointment(request,id):
        if request.user.is_superuser:
                if request.method=="POST":
                        form = ModifyAppointmentForm(request.POST)
                        appointment = Appointment.objects.get(id=id)
                        if form.is_valid():
                                date=form.cleaned_data['date']
                                initial_date=appointment.date
                                apps = Appointment.objects.filter(date=date)
                                if any(apps) or date < now():
                                        messages.error(request,'Enter A Valid Time!')
                                else:
                                        appointment.date=date
                                        appointment.save()
                                        send_mail(
                                                'Appointment With Dr. Serhal Modified!',
                                                f'Your appointment due on {initial_date} with Dr. Serhal has been moved to {appointment.date}.\nFor further contact us on 76784229.',
                                                settings.EMAIL_HOST_USER,
                                                [appointment.user.email,]
                                        )
                                        messages.success(request,'Appointment Successfully Modified!')
                                        return get_patient(request,appointment.user.username)
                        else:
                                messages.error(request,'Please Complete All Fields!')
                else:
                        form = ModifyAppointmentForm()
                return render(request,'admin/modify-app.html',{'form':form})        

                
def mark_as_missed(request,id):
        if request.user.is_superuser:
                appointment=Appointment.objects.get(id=id)
                appointment.missed=True
                appointment.save()
                return redirect(request.META['HTTP_REFERER'])
        else:
                redirect('login')

def metrics(request):
        if request.user.is_superuser:
                users=len(User.objects.filter(is_superuser=False))
                files=len(File.objects.all())
                online_appointments = len(Appointment.objects.filter(online=True))
                offline_appointments = len(Appointment.objects.filter(online=False))
                missed_online = len(Appointment.objects.filter(online=True,missed=True))
                missed_offline = len(Appointment.objects.filter(online=False,missed=True))
                online_appointments_percentage = round((online_appointments/(online_appointments+offline_appointments))*100,2)
                online_appointments_attendace_percentage = round(((online_appointments-missed_online)/online_appointments)*100,2)
                offline_appointments_percentage = round(((offline_appointments)/(online_appointments+offline_appointments))*100,2)
                offline_appointments_attendace_percentage = round(((offline_appointments-missed_offline)/offline_appointments)*100,2)
                online_to_offline_ratio = round(online_appointments/offline_appointments,2)

                context = {
                        'users':users,
                        'files':files,
                        'online_apps':online_appointments,
                        'offline_apps':offline_appointments,
                        'missed_online':missed_online,
                        'missed_offline':missed_offline,
                        'online_app_per':online_appointments_percentage,
                        'online_attendance_per':online_appointments_attendace_percentage,
                        'offline_app_per':offline_appointments_percentage,
                        'offline_attendance_per':offline_appointments_attendace_percentage,
                        'oor':online_to_offline_ratio
                }
                return render(request,'admin/metrics.html',context)
        else:
                redirect('login')