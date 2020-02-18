from django.urls import path , include
from rest_framework import routers
from employee.views import *

router = routers.DefaultRouter()
router.register('employee',EmployeeViewSet)
urlpatterns = [
    path('',include(router.urls)),
]
