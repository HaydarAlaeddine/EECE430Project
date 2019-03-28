from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Welcome {username}, you have successfully registered!')
            return redirect('login')
        else:
            messages.error(request,'Please complete all info')
    else:
        form=UserRegisterForm()
    return render(request,'users/signup.html', {'form':form})
