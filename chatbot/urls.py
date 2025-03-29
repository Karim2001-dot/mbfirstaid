from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('first-aid/', get_first_aid_response, name='first_aid'),
    path('first-aid-page/', first_aid_home, name='first_aid_page')
]
