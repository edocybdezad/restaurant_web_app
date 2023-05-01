"""
    homepage app Views
"""

from django.shortcuts import render, redirect

from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views import View

from django.contrib import messages
from django.core.mail import EmailMessage

from django.db.models import Sum

import datetime

from django.conf import settings

from .forms import ContactForm

from homepage.models import VisitorContact, Reservation, CloseReservation
from manager_tools.models import Item, Label, RestaurantInfo
import os

class HomePageView(TemplateView):
    template_name = "homepage/home.html"

class EatPageView(ListView):
    #--- shows restaurant menu items -food-
    #--- list of items implements an accordion style to help with navigation
    
    queryset = Label.objects.filter(pk__in = Item.objects.filter(section='EAT').values('label')).order_by('order')
    template_name = 'homepage/eat.html'
    
class DrinkPageView(ListView):
    #--- shows restaurant menu items -Drinks-
    #--- list of items implements an accordion style to help with navigation    
    
    queryset = Label.objects.filter(pk__in = Item.objects.filter(section='DRINK').values('label')).order_by('order')
    template_name = 'homepage/drink.html' 

class VisitPageView(View): 
    #--- shows restaurant info and contact form-
   
    template_name = 'homepage/visit.html'
    form_class = ContactForm
    
    def get(self, request, *args, **kwargs):
        print(os.environ.get('EMAIL_USER_OL'))
        print(os.environ.get('EMAIL_PASSWORD_OL'))
        form = self.form_class()
        restaurant = RestaurantInfo.objects.first()
        return render(request, self.template_name, {'form': form,
                                                    'restaurant': restaurant})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            eheader = f"Contact Form Via Web"
            sender_data = f"Sender : {form.cleaned_data['source'].upper()} \n Email : {form.cleaned_data['email']}\n Phone :  {form.cleaned_data['phone']}"
            subject = form.cleaned_data['subject']
            message = f"{eheader}\n {form.cleaned_data['message']}\n {sender_data}"
            sender = settings.EMAIL_HOST_USER
            recipients = [form.cleaned_data['email'], settings.EMAIL_HOST_USER]
            # send mail 
            email = EmailMessage(
                subject,
                message,
                sender,
                recipients,
            )
            email.send(fail_silently=False)
            
            # save contact form to db
            contact = VisitorContact(source=form.cleaned_data['source'], subject=subject, email=form.cleaned_data['email'], phone=form.cleaned_data['phone'], message=form.cleaned_data['message'])
            contact.save()
            print(form.cleaned_data)
            
            messages.success(request,"Your message have been received sucessfully")
            return redirect('home')

        return render(request, self.template_name, {'form': form})      

def reservation_form():
    # help function to create form fields 
    # according to restaurant open hours and reservation on web status
    
    closed_today = False
    currentday = datetime.datetime.today().date()
    reservation_status_today = CloseReservation.objects.get(pk=1)
    reservations_today = Reservation.objects.filter(day = currentday)
    reservations_pax_today = reservations_today.aggregate(Sum('persons'))
    
    if reservations_pax_today['persons__sum'] == None:
        reservations_pax_today['persons__sum'] = 0

    days = ['','Mon', 'Tue', 'Wed', 'Thu','Fri', 'Sat','Sun'] #isoweekday
    dt = datetime.datetime.now() 
    day = dt.isoweekday() #day of week as number 1 - 7
    
    if day == 1: # Restaurant is not open
        day += 1
    if dt.hour >= 15 and dt.minute > 10: # time limite for booking on web
        day += 1   
        
    hours = ['13:00','13:30','14:00','14:30','15:00','15:30']
    pax = ['1', '2', '3', '4','6','7','8','9','10']
    this_week = []
    
    for d in range(day,8):
        this_week.append({'day': days[d], 'date': f"{dt.day}-{dt.month}-{dt.year}"})
        dt = dt + datetime.timedelta(days=1)
        
    if reservation_status_today.closed or (reservations_pax_today['persons__sum'] >= reservation_status_today.limit):
        del this_week[0]
        closed_today = True
            
    next_week = []
    nw = datetime.datetime.now() + datetime.timedelta(days= 8 - day)
    for d in range(1,8):
        next_week.append({'day': days[d], 'date': f"{dt.day}-{dt.month}-{dt.year}"})
        nw = datetime.datetime.now() + datetime.timedelta(days=1)
    return {'this_week':this_week,
            'next_week': next_week,
            'hours':hours,
            'pax': pax}, closed_today

def reservation(request):
    # it manages reservation submision
    # send emails about the booking to restaurant mail and copy to customer email
    
    formf, closed_today = reservation_form()
    print(closed_today)
    if closed_today:
        messages.warning(request,'Reservations via web for today are closed. Try calling us') 
            
    if request.method == "POST":
        form_data = request.POST.dict()
        day_str = form_data.get('days')
        day = datetime.datetime.strptime(day_str, "%d-%m-%Y").date()
        hour = form_data.get('hours')
        pax = int(form_data.get('pax'))
        note = form_data.get('notes')
        name = form_data.get('name')
        email = form_data.get('email')
        phone = form_data.get('phone')
        
        #send booking info to email and a copy to user mail
        sender = settings.EMAIL_HOST_USER
        recipients = [email, settings.EMAIL_HOST_USER]
        subject = f"Table reservation recieved via web"
        message = f"day : {day_str}\n Persons : {pax}\n Hour : {hour}\n Note: {note}\n Customer Info:\n Name: {name}\n Email: {email}\n Phone: {phone}"
        email = EmailMessage(
            subject,
            message,
            sender,
            recipients,
        )
        email.send(fail_silently=False)
                
        print(type(day), hour, pax, note, name, email, phone)
        reservation = Reservation(day=day, hour=hour, persons=pax, note=note, user=name, email=email, phone=phone)
        print('FORM READY TO SUBMIT', form_data)
        reservation.save()
        messages.success(request,"Your reservation have been received sucessfully")
        return redirect('home')
    return render(request, 'homepage/booking.html', formf)   