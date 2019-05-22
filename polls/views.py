import logging, logging.config
import sys
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Choice, Question
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import generic
from rest_framework.decorators import api_view
import csv
from .forms import QuestionForm, ChoicesForm
from django.utils import timezone
from django.forms import modelformset_factory

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    choice_list= Choice.objects.order_by('word')
    context = {'latest_question_list': latest_question_list, 'choice_list': choice_list}
    return render(request, 'polls/index.html', context)

#class DetailView(generic.ListView):
#   model = Question
#  template_name = 'polls/detail.html'
# question = get_object_or_404(Question, pk=question_id)



def detail(request, question_id):
    logger = logging.getLogger(__name__)
    logger.error('Hay un problema con el id')#funciona, ponemos asi los logs
    question = get_object_or_404(Question, pk=question_id)
    id_question=question.id
    print(f"El texto de la pregunta en cuestion es: {question.question_text}")
    choices= dict()
    suma = 0
    suma_true=0
    type_choice=question.question_type
    print(type_choice)

    for question_list in question.choice_set.all():
        choices[question_list.choice_text] = question_list.votes
        suma +=question_list.votes
        if question_list.is_correct_answer is True and question_list.votes > 0:
            print(f"Numero de respuestas correctas: {question_list.votes}")
            suma_true = question_list.votes
        suma_wrong=suma-suma_true
    return render(request, 'polls/detail.html', {'question': question,'choices' :choices,'sum': suma, 'type_choice': type_choice, 'suma_true': suma_true,'suma_wrong':suma_wrong})

#def results(request, question_id):
 #   question = get_object_or_404(Question, pk=question_id)
  #  return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(f"request {request}")
    print(f"request.POST {request.POST}")
    pk = request.POST['choice']
    try:
        print("******El ID de la pregunta que hemos votado"+ pk)
        print(f"request.POST['choice'] {request.POST['choice']}")
        print(f"question.question_text {question.question_text}")
        print(question.choice_set.all().values())
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

        #selected_choice = question.choice_set.get(pk="1")

    except (KeyError, Choice.DoesNotExist) as e:
        print(e)
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

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html',{
        'form': form
    })

class ChartData(APIView):
    authentication_classes= []
    permission_classes = []

    def get(self,request,format= None):
        resultado = dict()
        # pk: es id de question, pasarlo x get
        # Choice.objects.all() --> Choice.objects.filter(question__id=pk)

        for choice in Choice.objects.all():
            print(f"numero de votos de {choice.choice_text}: {choice.votes}  ")
            resultado[choice.choice_text] = choice.votes

        dic_resultados = dict(resultado)

        data = {
            "respuestas": dic_resultados.keys(),
            "votos": dic_resultados.values()
        }



        return Response(data)


def export_csv(request,question_id):



    question_object = get_object_or_404(Question, pk=question_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= "Resultados: ' + question_object.question_text + '.csv"'
    writer = csv.writer(response, delimiter=';', dialect='excel')
    total_votes = 0
    correct_votes = 0
    wrong_answers = 0

    print(f"question_type en export_csv: {question_object.question_type}")
    if question_object.question_type == 'E':
        writer.writerow(['Respuestas', 'Votos'])
        for choices in question_object.choice_set.all():
            writer.writerow([choices.choice_text, choices.votes])
            total_votes += choices.votes
            print(f"numero total de votos exportados: {total_votes}")
        writer.writerow(['Total', total_votes])
    else:
        if question_object.question_type == 'T':
            writer.writerow(['Respuestas', 'Votos'])
            for choices in question_object.choice_set.all():
                writer.writerow([choices.choice_text, choices.votes])
                total_votes += choices.votes
                print(f"numero total de votos del test exportados: {total_votes}")
                if choices.is_correct_answer is True:
                    correct_votes = choices.votes

            writer.writerow(['Total', total_votes])
            wrong_votes = total_votes - correct_votes
            writer.writerow(['', ''])
            writer.writerow(['Votos a la respuesta Correcta: ', correct_votes])
            writer.writerow(['Votos a la respuesta Incorrecta: ', wrong_votes])





    return response


def post_question(request):
    choices_formset = modelformset_factory(Choice, form=ChoicesForm, fields=('choice_text', 'is_correct_answer'),
                                           extra=3)
    if request.method == "POST" or request.method == "post":
        question_form = QuestionForm(request.POST)
        choice_form = choices_formset(request.POST, request.FILES)
        for form_ in choice_form:
            print(form_.as_table())

        if question_form.is_valid and choice_form.is_valid:
            post = question_form.save(commit=False)
            question_id = post.id
            post.save()
           # choice_form = choices_formset(queryset=Choice.objects.all())
            for form in choice_form:
                choice = form.save(commit=False)
                question = get_object_or_404(Question, pk=question_id)
                choice.question = question
                choice.save()

            return HttpResponseRedirect(reverse('polls:index'))
           # return redirect('create_answer', question_id)
    else:
        form = QuestionForm()
        choices_formset = modelformset_factory(Choice, form=ChoicesForm, fields=('choice_text', 'is_correct_answer'), extra=3)
        #form = choices_formset()
        #form = ChoicesForm()
        choice_form= choices_formset(queryset=Choice.objects.none(),)
        return render(request, 'polls/create_question.html', {'form': form, 'choice_form': choice_form})

def post_answer(request,question_id):
    choices_formset = modelformset_factory(Choice, form=ChoicesForm, fields=('choice_text','is_correct_answer'), extra=3)
    if request.method == "POST":
        #form = ChoicesForm(request.POST)
        choice_form = choices_formset(request.POST, request.FILES)

        if choice_form.is_valid:
            for form in choice_form:
                choice = form.save(commit=False)
                question = get_object_or_404(Question, pk=question_id)
                choice.question = question
                choice.save()

            return HttpResponseRedirect(reverse('polls:index'))
    else:
        choices_formset = modelformset_factory(Choice, form=ChoicesForm, fields=('choice_text', 'is_correct_answer'), extra= 3)
        #form = choices_formset()
        #form = ChoicesForm()
        form= choices_formset(queryset=Choice.objects.none(),)
        return render(request, 'polls/create_answer.html', {'form': form})

def results(request):
    users = User.objects.values_list('username',flat= True)
    user_list= []
    user_count = 0
    for user in users:
        print(user)
        user_list.append(user)
        user_count +=1


    return render(request, 'polls/results.html', {'user_list': user_list,'user_count': user_count})

def users_list(request):
    users = User.objects.values_list('username',flat= True)
    user_list= []
    user_count = 0
    for user in users:
        print(user)
        user_list.append(user)
        user_count +=1
    return render(request, 'polls/users_list.html',{'users_list': user_list,'user_count': user_count})
