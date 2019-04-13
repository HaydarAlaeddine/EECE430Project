from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, AppointmentForm
from .models import Appointment,Profile
from django.contrib.auth.models import User



# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.address = form.cleaned_data.get('address')
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.record.date_of_birth = form.cleaned_data.get('date_of_birth')
            user.record.medical_history = form.cleaned_data.get('medical_history')
            user.record.blood_type = form.cleaned_data.get('blood_type')
            user.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
        else:
            messages.error(request,'Please complete all info')
    else:
        form=UserRegisterForm()
    return render(request,'users/signup.html',{'form':form})

def take_appointment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form=AppointmentForm(request.POST)
            if form.is_valid():
                appointment = form.save(commit=False)
                appointments=Appointment.objects.filter(date=appointment.date)
                if any(appointments):
                    messages.error(request,'This time is already taken')
                    
                else :
                    user = User.objects.get(username=request.user.username)
                    appointment.user=user
                    appointment.save()
                    return redirect('homepage')
                
            else:
                messages.error(request,'Please complete all info')
        else:
            form=AppointmentForm()
        return render(request,'users/appointment.html',{'form':form})
    else :
        return redirect('login')

def view_profile(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        user_profile=Profile.objects.get(user=user)
        context = {
            "profile":user_profile,
            "user":user
        }
        return render(request,'users/profile.html',context)
    else:
        redirect('login')
