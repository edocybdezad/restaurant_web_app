"""
    manager_tools app Views
"""

from django.shortcuts import render,redirect
from django.urls import reverse_lazy


from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.contrib import messages



from .models import *
from .forms import ItemForm, ListReservationForm, AddReservationForm
from homepage.models import Reservation, CloseReservation

from .utilities import make_from_tsv

from django.contrib.auth.mixins import LoginRequiredMixin 

class IndexView(LoginRequiredMixin, TemplateView):
    #--- Template showing this app options
    login_url = 'manager/login/'
    template_name = 'manager_tools/index.html'
 
    
class ItemList(LoginRequiredMixin,ListView):
    #--- List of restaurant menu items by category(Label model)
    #--- each of this listed items are links to an Update Form(ItemUpdate)

    model = Item   
    queryset = Label.objects.all().order_by('order')
    template_name = "manager_tools/item_list.html"

class ItemUpdate(LoginRequiredMixin, UpdateView):
    #---- Via form we can edit a menu item info
    
    model = Item
    form_class = ItemForm
    template_name = "manager_tools/update_item.html"
    success_url = "/eat/"

class RestaurantInfo(LoginRequiredMixin,UpdateView):
    #--- Single row model allows to change open hours and add some
    #--- updates about events. 
    
    model = RestaurantInfo
    fields = '__all__'
    template_name = 'manager_tools/restaurant_info_form.html'
    success_url = '/visit/'
    
class ReservationsClose(LoginRequiredMixin,UpdateView):
    #----View allows to stop allowing reservations via web by marking a field to close
    #----or modifying a limit of persons in total
    
    model = CloseReservation
    fields = '__all__'
    template_name = 'manager_tools/reservation_close_form.html'
    success_url = '/reservation'

class ListReservations(LoginRequiredMixin,View):
    #---- Accept a date via form submission to request a list of reservations for that date
    #---- by default shows a list of reservation for current date. 
    template_name = 'manager_tools/reservations_list.html'
    form_class = ListReservationForm
    
    def get(self, request, *args, **kwargs):
        reservations = Reservation.objects.all().order_by('-day')
        return render(request, self.template_name, {'form': self.form_class,
                                                    'reservations':reservations})
    
    def post(self, request, *args, **kwargs):
        
        form = self.form_class(request.POST)
        if form.is_valid():
            rdate = form.cleaned_data['rdate']
            print(rdate)
            reservations = Reservation.objects.filter(day=rdate).all()
            return render(request, self.template_name, {'form': form,
                                                        'reservations': reservations})

        return render(request, self.template_name, {'form': form})     
      
class AddReservation(LoginRequiredMixin,CreateView):
    #--- Add a object to Reservation model this have to works even
    #--- if reservation are closed.
    
    model = Reservation
    form_class = AddReservationForm
    template_name = 'manager_tools/add_reservation.html'
    success_url = reverse_lazy('manager_tools:list_reservations') # redirect to reservation list to check the new reservations

def UpdateMenu(request):
    # Upload a .tsv file that contains a new menu including food and drink
    # only .tsv file is allowed
    
    new_menu = []
    menu_labels = []
    
    if request.method == "POST":
        file_up = request.FILES["menufile"]
        ext = file_up.name[-3:]
        if ext == 'tsv':
            new_menu = make_from_tsv(file_up)
        else:
            messages.warning(request,"Invalid File Format. A .tsv file is required")
            return render(request,"manager_tools/import.html")
        
        # ----- New menu will be created from empty db -- #
        m_items = Item.objects.all()
        m_labels = Label.objects.all()
        if m_items:
            m_items.delete()
        if m_labels:
            m_labels.delete()
            
        # --- building menu from .tsv file ---#
        
        # --- unique labels for Label model --- #
        for line in new_menu:
            if line['label'] not in menu_labels:
                menu_labels.append(line['label'])
            
        #--- Create Label object from the new_menu elements
        
        order = 1 # order of listing on menu
        for label in menu_labels:
            l = Label(name=label, order=order) 
            l.save()
            order += 1
            
        # --- Create menu. Items objects one object per row with an item coming from imported .tsv file
        # --- and relating them with before created labels
        
        for line in new_menu:
            i = Item(name=line['name'], description=line['description'], price=line['price'], section=line['section'], label=Label.objects.filter(name=line['label']).first())
            i.save()
            
        # -- redirect to homepage eat page to see how the result on food items.
        
        return redirect("eat")

    return render(request,"manager_tools/update_menu.html")