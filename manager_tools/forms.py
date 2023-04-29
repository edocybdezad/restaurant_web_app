"""
    manager_tools Forms
"""
from django import forms
from django.forms import ModelForm

from manager_tools.models import Item
from homepage.models import Reservation

class ItemForm(ModelForm):
    class Meta:
        DISPONIBLE = True
        NO_DISPONIBLE = False
        
        av = [(DISPONIBLE,'DISPONIBLE'),(NO_DISPONIBLE,'NO DISPONIBLE')]        
        model = Item
        fields = ['name', 'description', 'price', 'available']
        
        widgets = {

            'available' : forms.Select(choices= av),
            
        }

class AddReservationForm(ModelForm):
    class Meta:
        REGULAR = 'REGULAR'
        EVENT = 'EVENT'
        
        R_TYPE = [(REGULAR,'REGULAR'),(EVENT,'EVENT')]        
        model = Reservation
        fields = ['day', 'hour', 'persons', 'note', 'user', 'email','phone','r_type']
        
        labels = {
            'user':'Name',
            'r_type':'Tipo de Reserva'
        }
        
        widgets = {
            'day' : forms.DateInput(attrs={'type':'date'}),
            'note' : forms.Textarea(attrs={'rows':'4'}),
            'hour' : forms.TimeInput(attrs={'type':'time', 'min':'12:00'}),
            'r_type' : forms.Select(choices= R_TYPE),  
        }
        

class ListReservationForm(forms.Form):
    rdate = forms.DateField(label='List Reservation by Date', widget=forms.DateInput(attrs={"type":"date"}))
    

