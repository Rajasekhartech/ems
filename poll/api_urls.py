from django.urls import path
from poll.views import *
urlpatterns = [
    path('poll/',Poll),
    path('poll/<int:id>/',Poll_details),
]
