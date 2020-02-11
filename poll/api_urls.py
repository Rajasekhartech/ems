from django.urls import path
from poll.views import *
urlpatterns = [
    path('poll/',Poll),
]
