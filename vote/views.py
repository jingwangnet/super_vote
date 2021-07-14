from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        if request.POST.get('new-question'):
            Question.objects.create(text=request.POST['new-question'])
            return redirect('/')
         
    context = {
        'new_question': Question.objects.first().text if Question.objects.first() else '',
        'new_vote': request.POST.get('new-vote', '')
    }
    return render(request, 'vote/index.html', context)
