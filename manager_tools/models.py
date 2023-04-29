"""
    manager_tools app Models
"""

from django.db import models

# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     pass

class Label(models.Model):
    name = models.CharField(max_length=30)
    order = models.IntegerField(null=True) 
    def __str__(self):
        return f"{self.order} - {self.name}"
  
class Item(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=120, blank=True)
    price = models.CharField(max_length=8) #no calculations with this item
    available = models.BooleanField(default=True)
    section = models.CharField(max_length=10)
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name='label_items')

      
class RestaurantInfo(models.Model):
    #--- Restaurant Info ----#
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=100)
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    open_hours = models.TextField()
    insta = models.URLField(blank=True, null=True)
    face = models.URLField(blank=True,null=True)


    
