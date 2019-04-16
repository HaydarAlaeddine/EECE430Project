from django.urls import path, include 
from .views import view_patients,get_patient,get_appointments
urlpatterns = [
    path('patients/', view_patients,name='patients'),
    path('patients/<str:username>',get_patient,name='patient-details'),
    path('appointments/',get_appointments,name='appointments')
]
