from django.contrib import admin

# Register your models here.
from .models import Patient, PatientRecord

admin.site.register(Patient)
admin.site.register(PatientRecord)