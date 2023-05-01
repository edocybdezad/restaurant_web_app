"""
    homepage app Urls
"""
from django.urls import path

from homepage.views import (
    HomePageView,
    EatPageView,
    DrinkPageView,
    VisitPageView,
)
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', HomePageView.as_view(), name='home'),
    path('eat/', EatPageView.as_view(), name='eat'),
    path('drink/', DrinkPageView.as_view(), name='drink'),
    path('visit/', VisitPageView.as_view(), name='visit'),
    #--- reservation view receives ajax post request
    path('reservation',views.reservation, name='reservation' )
]