from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question, Vote

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        if request.POST.get('new-question'):
            Question.objects.create(text=request.POST['new-question'])
            return redirect('/')
        if request.POST.get('new-vote'):
            Vote.objects.create(text=request.POST['new-vote'])
            return redirect('/')
         
    context = {
        'new_question': Question.objects.first().text if Question.objects.first() else '',
        'votes': Vote.objects.all() 
    }
    return render(request, 'vote/index.html', context)
