from django.urls import path
from poll.views import *
urlpatterns = [
    path('poll/',PollListView.as_view()),
    path('poll/<int:id>/',PollListView.as_view()),
]
