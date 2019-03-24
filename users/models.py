from django.db import models

# Create your models here.
class PatientRecord(models.Model):
    record_id = models.IntegerField(primary_key=True)
    date_of_birth = models.DateField()
    blood_type = models.CharField(max_length=3)
    
    def __str__(self):
        return f'patient id: {self.patient_id}'


class Patient(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=8)
    patient_id=models.IntegerField(primary_key=True )
    record=models.ForeignKey(PatientRecord,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'