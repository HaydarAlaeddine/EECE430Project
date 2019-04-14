from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.utils.timezone import now

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=8)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} '

class Record(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=date.today)
    blood_type = models.CharField(max_length=3)
    medical_history = models.CharField(max_length=5000)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} '

class Appointment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(default=now())
    def __str__(self):
        return f'{self.date}'

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Record.objects.create(user=instance)
    instance.profile.save()
    instance.record.save()