from django.urls import path
from .views import *

urlpatterns = [
    path('home/', list_view, name='home'),
]