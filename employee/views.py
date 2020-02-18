from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.auth.models import User
from employee.forms import UserForm
from django.contrib.auth import authenticate, logout,login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.sessions.models import Session
from ems.decorators import admin_hr_required
from django.views.generic import DeleteView
from django.views.generic.edit import UpdateView

from employee.serializers import EmployeeSerializer
from rest_framework import viewsets
# Create your views here.

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = EmployeeSerializer


def home(request):
    return render(request, 'home.html')

def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            if request.GET.get('next', None):
                request.session['id'] = user.id
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('employee_list'))


        else:
            context['error'] = "Provide valid credentials !!!"
            return render(request, "auth/login.html", context)
    else:
        return render(request, "auth/login.html", context)

@login_required(login_url= '/login/')
def user_success(request):
    context = {}
    context['user'] = request.user
    return render(request, "auth/success.html", context)

#@login_required(login_url= '/login/')
def user_logout(request):
    if request.method=="POST":
        logout(request)
        return HttpResponseRedirect(reverse('user_login'))

@login_required(login_url= '/login/')
def employee_list(request):
    context = {}
    context['users'] = User.objects.all()
    context['title'] = 'Employees'
    return render(request, 'employee/index.html',context)


@login_required(login_url= '/login/')
def employee_details(request, id = None):
    context = {}
    context['user'] = get_object_or_404(User, id = id)
    return render(request,'employee/details.html',context)

@login_required(login_url= '/login/')
@admin_hr_required
def employee_add(request):
    context = {}
    if request.method == "POST":
        user_form = UserForm(request.POST)
        context['user_form'] = user_form
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request,'employee/add,html', context)



    else:
        user_form = UserForm()
        context['user_form'] = user_form
        return render(request, 'employee/add.html',context)

@login_required(login_url= '/login/')
def employee_edit(request, id =id):
    user = get_object_or_404(User, id = id)
    if request.method == "POST":
        user_form = UserForm(request.POST , instance = user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request,'employee/edit.html',{"user_form" : user_form})

    else:
        user_form = UserForm(instance =user)
        return render(request, 'employee/edit.html',{"user_form" : user_form})

def employee_delete(request , id = None):
    user = get_object_or_404(User, id = id)
    if request.method == "POST":
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        context={}
        context['user'] = user
        return render(request, 'employee/delete.html', context)

class ProfileUpdate(UpdateView):
    fields = ['designation', 'salary']
    template_name = 'auth/profile_update.html'
    success_url = reverse_lazy('my_profile')
    def get_object(self, queryset=None):
        return self.request.user.profile


class MyProfile(DeleteView):
    template_name = 'auth/profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from rest_framework.response import Response
from django.contrib.auth import login as django_login , logout as django_logout
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class LogoutView(APIView):
    # authentication_classes = (TokenAuthentication, )
    #
    # def post(self, request):
    #     django_logout(request)
    #     return Response(status=204)
    pass