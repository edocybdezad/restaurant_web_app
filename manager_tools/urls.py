"""
    manager_tools app Urls
"""
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView

from manager_tools.views import (
    IndexView,
    RestaurantInfo,
    ItemList,
    ItemUpdate,
    ReservationsClose,
    AddReservation,
    ListReservations,

)

from . import views

app_name = 'manager_tools'

urlpatterns = [
    path('', IndexView.as_view(), name='manager'),
    path('update_menu/', views.UpdateMenu, name='update_menu'),
    path('restaurant_info/<int:pk>', RestaurantInfo.as_view(), name='restaurant_info'),
    path('items_list/', ItemList.as_view(), name='items_list'),
    path("<int:pk>", ItemUpdate.as_view(), name="item-update"),
    path("close_day/<int:pk>", ReservationsClose.as_view(), name="close_day"),
    path("add_reservation/", AddReservation.as_view(), name="add_reservation"),
    path("list_reservations/", ListReservations.as_view(), name="list_reservations"),
    #---- auth ----#
    path("manager/login/", LoginView.as_view(template_name='manager_tools/login.html'), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),     
]