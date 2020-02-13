from django.shortcuts import render, get_object_or_404 , redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from poll.models import *
from django.http import Http404 , HttpResponse
from  django.contrib.auth.decorators import login_required
from ems.decorators import admin_hr_required
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from poll.forms import PollForm, ChoiceForm
from poll.serializers import QuestionSerializer

from rest_framework.parsers import JSONParser
# Create your views here.

@csrf_exempt
def Poll(request):
    if request.method == "GET":
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many= True)
        return JsonResponse(serializer.data, safe= False)
    elif request.method == "POST":
        json_parser = JSONParser()
        data = json_parser.parse(request)
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status= 400)

@csrf_exempt
def Poll_details(request, id):
    try:
        instance = Question.objects.get(id = id)
    except Question.DoesNotExist as e:
        return JsonResponse({"error" : "Given question object not found"}, status= 404)

    if request.method == "GET":
        serializer = QuestionSerializer(instance)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        json_parser = JSONParser()
        data = json_parser.parse(request)
        serializer = QuestionSerializer(instance, data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status= 400)
    elif request.method == "DELETE":
        instance.delete()
        return HttpResponse(status=204)

@login_required(login_url= '/login/')
def index(request):
    context = {}
    questions = Question.objects.all()
    context['questions'] = questions
    context['title'] = 'polls'
    return render(request,'polls/index.html', context)

@login_required(login_url= '/login/')
def details(request, id = None):
    context = {}
    try:
        question = Question.objects.get(id = id)
    except:
        raise Http404

    context['question'] = question
    return render(request,'polls/details.html', context)


@login_required(login_url= '/login/')
def poll(request, id = None):
    if request.method == "GET":
        try:
            question = Question.objects.get(id=id)
        except:
            raise Http404
        context = {}
        context['question'] = question
        return render(request, 'polls/poll.html', context)
    if request.method == "POST":
        user_id = 1
        data = request.POST
        ret = Answer.objects.create(user_id = user_id, choice_id=data['choice'])
        if ret:
            return HttpResponse("Your vote is done succesfully")
        else:
            return HttpResponse("Your vote is not done sucessfully")

class PollView(View):
    decorators = [login_required, admin_hr_required]

    @method_decorator(decorators)
    def get(self, request, id=None):
        if id:
            question = get_object_or_404(Question, id=id)
            poll_form = PollForm(instance=question)
            choices = question.choice_set.all()
            choice_forms = [ChoiceForm(prefix=str(
                choice.id), instance=choice) for choice in choices]
            template = 'polls/edit_poll.html'
        else:
            poll_form = PollForm(instance=Question())
            choice_forms = [ChoiceForm(prefix=str(
                x), instance=Choice()) for x in range(3)]
            template = 'polls/new_poll.html'
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, template, context)

    @method_decorator(decorators)
    def post(self, request, id=None):
        context = {}
        if id:
            return self.put(request, id)
        poll_form = PollForm(request.POST, instance=Question())
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            x), instance=Choice()) for x in range(0, 3)]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return HttpResponseRedirect('/poll')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'polls/new_poll.html', context)

    @method_decorator(decorators)
    def put(self, request, id=None):
        context = {}
        question = get_object_or_404(Question, id=id)
        poll_form = PollForm(request.POST, instance=question)
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            choice.id), instance=choice) for choice in question.choice_set.all()]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return redirect('polls_list')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'polls/edit_poll.html', context)

    @method_decorator(decorators)
    def delete(self, request, id=None):
        question = get_object_or_404(Question, id = id)
        print(question)
        question.delete()
        return redirect('polls_list')