from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from employee.forms import UserForm
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def employee_list(request):
    context = {}
    context['users'] = User.objects.all()
    context['title'] = 'Employees'
    return render(request, 'employee/index.html',context)
def employee_details(request, id = None):
    context = {}
    context['user'] = get_object_or_404(User, id = id)
    return render(request,'employee/details.html',context)
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