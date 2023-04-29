"""
    Homepage app Models
"""
from django.db import models


class VisitorContact(models.Model):
    source = models.CharField(max_length=50)
    subject = models.CharField(max_length= 60)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.source}, {self.subject}, {self.message}' 
    
class Reservation(models.Model):   
    day = models.DateField()
    hour = models.TimeField()
    persons = models.IntegerField()
    note = models.TextField()
    user = models.CharField(max_length=60)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    r_type = models.CharField(max_length=7, default='REGULAR')
    created_at = models.DateField(auto_now_add=True)
    
class CloseReservation(models.Model):
    closed = models.BooleanField(default=False)
    limit = models.IntegerField(blank=True, null=True, default=50)

