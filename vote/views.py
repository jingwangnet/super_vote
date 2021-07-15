from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question, Vote

# Create your views here.
def home_page(request):
    questions = Question.objects.all()
    context = {'questions': questions}
    return render(request, 'vote/index.html', context)

def new_question(request):
    question = Question.objects.create(text=request.POST['new-question'])
    return redirect(f'/question/{question.pk}/')

def view_question(request, pk):
    question = Question.objects.get(pk=pk)
    context = {'question': question}
    return render(request, 'vote/question.html', context)

def new_vote(request, pk):
    question = Question.objects.get(pk=pk)
    Vote.objects.create(text=request.POST['new-vote'])
    return redirect(f'/question/{question.pk}/result/')

def view_vote(request,pk):
    votes = Vote.objects.all()
    question = Question.objects.get(pk=pk)
    context = {
        'new_question':  question.text,
        'votes': votes
    }
    return render(request, 'vote/vote.html', context)

