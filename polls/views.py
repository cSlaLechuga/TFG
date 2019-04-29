import logging, logging.config
import sys
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice, Question
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    choice_list= Choice.objects.order_by('word')
    context = {'latest_question_list': latest_question_list, 'choice_list': choice_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    logger = logging.getLogger(__name__)
    logger.error('Hay un problema con el id')#funciona, ponemos asi los logs
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Por favor, seleccione una opción",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:index'))
    # return HttpResponseRedirect(reverse('polls:index', args=(question.id,)))