from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

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
            messages.success(request,f'Welcome {username}, you have successfully registered!')
            return redirect('login')
        else:
            messages.error(request,'Please complete all info')
    else:
        form=UserRegisterForm()
    return render(request,'users/signup.html',{'form':form})
