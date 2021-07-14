from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    context = {
        'new_question': request.POST.get('new-question', ''),
        'new_vote': request.POST.get('new-vote', '')
    }
    return render(request, 'vote/index.html', context)
