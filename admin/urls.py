from django.urls import path, include 
from .views import view_patients,get_patient,get_appointments, add_appointments,delete_appointment,modify_appointment,mark_as_missed
urlpatterns = [
    path('patients/', view_patients,name='patients'),
    path('patients/<str:username>',get_patient,name='patient-details'),
    path('appointments/',get_appointments,name='appointments'),
    path('add-appointments/',add_appointments,name='add-appointments'),
    path('appointments/delete/<int:id>',delete_appointment,name='delete'),
    path('appointments/modify/<int:id>',modify_appointment,name='modify'),
    path('appointments/mark-as-missed/<int:id>',mark_as_missed,name='mark-as-missed')
]
