from django.urls import path
from poll.views import *
urlpatterns = [
    path('',index , name = 'polls_list'),
    path('<int:id>/details', details, name = 'polls_details'),
    path('<int:id>/', poll, name = 'single_poll'),
]
