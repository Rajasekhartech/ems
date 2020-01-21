from  poll.models import Question
from django.contrib.auth.models import User

def poll_count(request):
    count = Question.objects.count()
    return {"polls_count" : count}
def emp_count(request):
    count = User.objects.count()
    return {"emp_count" : count}