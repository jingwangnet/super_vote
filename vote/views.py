from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question, Vote

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        if request.POST.get('new-question'):
            Question.objects.create(text=request.POST['new-question'])
            return redirect('/question/the-only-url/')
        if request.POST.get('new-vote'):
            Vote.objects.create(text=request.POST['new-vote'])
            return redirect('/question/the-only-url/result/')
         
    context = {
        'new_question': Question.objects.first().text if Question.objects.first() else '',
        'votes': Vote.objects.all() 
    }
    return render(request, 'vote/index.html', context)

def new_question(request):
    Question.objects.create(text=request.POST['new-question'])
    return redirect('/question/the-only-url/')

def view_question(request):
    context = {
        'new_question': Question.objects.first().text
    }
    return render(request, 'vote/question.html', context)

def view_vote(request):
    votes = Vote.objects.all()
    context = {
        'new_question': Question.objects.first().text,
        'votes': votes
    }
    return render(request, 'vote/vote.html', context)

