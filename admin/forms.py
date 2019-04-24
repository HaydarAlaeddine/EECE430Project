from django import forms
from django.contrib.auth.models import User
from users.models import Appointment

class RequestDocumentForm(forms.Form):
    description = forms.CharField()
    class Meta:
        fields = ['description']

class AppointmentForm(forms.ModelForm):
    users = User.objects.values_list('username','username').filter(is_superuser=False)
    date = forms.DateTimeField(help_text='Required Format: MM/DD/YYYY')
    users_field = forms.CharField(widget=forms.Select(choices=users))
    class Meta:
        model = Appointment
        fields=['users_field','date']
      
    
    def save(self, commit=True):
        appointment = super(AppointmentForm, self).save(commit=False)
        appointment.date = self.cleaned_data["date"]
        
        if commit:
            appointment.save()
        return appointment

class ModifyAppointmentForm(forms.Form):
    date = forms.DateTimeField(help_text='Required Format: MM/DD/YYYY')
    class Meta:
        fields=['date']