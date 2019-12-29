from  poll.models import Question

def poll_count(request):
    count = Question.objects.count()
    return {"polls_count" : count}