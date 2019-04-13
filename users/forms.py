from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Appointment
class UserRegisterForm(UserCreationForm):
    blood_type_choices= [
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ]


    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    address = forms.CharField()
    phone_number = forms.CharField()
    date_of_birth = forms.DateField(help_text='Required Format: MM-DD-YYYY')
    blood_type = forms.CharField(widget=forms.Select(choices=blood_type_choices))
    medical_history = forms.CharField()
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'date_of_birth','medical_history','phone_number','blood_type','medical_history' , 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user

class AppointmentForm(forms.ModelForm):
    date = forms.DateTimeField()

    class Meta:
        model = Appointment
        fields=['date']
    
    def save(self, commit=True):
        appointment = super(AppointmentForm, self).save(commit=False)
        appointment.date = self.cleaned_data["date"]
        
        if commit:
            appointment.save()
        return appointment