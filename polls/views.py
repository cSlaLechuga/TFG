import logging, logging.config
import sys
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Choice, Question, Profile, Asignaturas
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import generic
from rest_framework.decorators import api_view
import csv
from .forms import QuestionForm, ChoicesForm, SignUpForm, ModelForm_Teacher, inlineformset_factory, ChoicesForm_T, ChoicesForm_E, Input_Answer
from django.utils import timezone
from django.forms import modelformset_factory
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaulttags import register
from .filters import ChoiceFilter
from .utils import render_to_pdf
from django.template.loader import get_template


@login_required
def index(request):
    TextFormset_dict = dict()
    latest_question_list_text_type = Question.objects.filter(question_type = 'D')
    for list_text_type in latest_question_list_text_type:
        TextFormset_dict[list_text_type] = Input_Answer()

    latest_question_list_poll = Question.objects.filter(question_type = 'E')
    latest_question_list_test = Question.objects.filter(question_type = 'T')
    choice_list= Choice.objects.order_by('word')
    context = {'latest_question_list_test': latest_question_list_test, 'latest_question_list_poll': latest_question_list_poll,'TextFormset_dict': TextFormset_dict, 'choice_list': choice_list}
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
    choices= voters_list =dict()
    suma = 0
    suma_true = suma_wrong = 0
    list_voters = []
    type_choice=question.question_type
    print(type_choice)

    for question_list in question.choice_set.all():
        choices[question_list.choice_text] = question_list.votes
        suma +=question_list.votes
        if question_list.is_correct_answer is True and question_list.votes > 0:
            print(f"Numero de respuestas correctas: {question_list.votes}")
            suma_true = question_list.votes
        suma_wrong=suma-suma_true
    #Ponerlo SOLO CUANDO SEA TEST
    if question.question_type == 'T':
        #Aqui procedemos a enviar a la plantilla un diccionario de listas con la gente que ha votado
        for choice in question.choice_set.all():
            voters = choice.who_voted
            if voters != None:
                voters = voters.split(',')
                if '' in voters:
                    voters.remove('')
                elif ' ' in voters:
                    voters.remove(' ')

            print(type(choice.choice_text))
            voters_list[choice.choice_text] = {'voters':voters}
            print(f"Lo que pasamos a la plantilla con preguntas y votantes: {voters_list}")


    return render(request, 'polls/detail.html', {'question': question,'choices' :choices,'sum': suma, 'type_choice': type_choice, 'suma_true': suma_true,'suma_wrong':suma_wrong,'voters_list': voters_list})

#def results(request, question_id):
 #   question = get_object_or_404(Question, pk=question_id)
  #  return render(request, 'polls/results.html', {'question': question})
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Profesores').count() == 0)
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.question_type == 'D':
        if request.method == 'POST':
            form = Input_Answer(request.POST, instance=question)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('polls:index'))



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
        if question.question_type == 'T':
            profile = get_object_or_404(Profile, pk=request.user.pk)
            print(f"El usuario que ha votado es: {profile.nombre + ' ' + profile.apellido}")
            who_voted = ''
            if selected_choice.who_voted is None:
                who_voted = ''
                who_voted = profile.nombre + ' ' + profile.apellido
            else:
                who_voted = selected_choice.who_voted
                who_voted =who_voted +  ','+ profile.nombre + ' ' + profile.apellido
            selected_choice.who_voted = who_voted
            selected_choice.save()
            print(f"Listado de usuarios que han votado: {who_voted}")

            profile.total_votes += 1
            profile.save()
            if selected_choice.is_correct_answer:
                profile.total_votes_OK += 1
                profile.save()
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
    return render(request, 'registration/signup_teacher.html',{
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
    #form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            question_id = post.id
            post.creator = str(User.objects.get(username=request.user))
            post.save()



            return redirect('polls:post_answer', question_id = question_id)


    else:
        form = QuestionForm()


    return render(request,'polls/create_question.html', {'form': form})

#
# def post_answer(request,question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     choices_formset = modelformset_factory(Choice, form=ChoicesForm, fields=('choice_text','is_correct_answer'), extra=question.n_choices)
#     if request.method == "POST":
#         #form = ChoicesForm(request.POST)
#         choice_form = choices_formset(request.POST, request.FILES)
#
#         if choice_form.is_valid:
#             for form in choice_form:
#                 choice = form.save(commit=False)
#                 choice.question = question
#                 choice.save()
#
#             return HttpResponseRedirect(reverse('polls:index'))
#     else:
#         #choices_formset = modelformset_factory(Choice, form=ChoicesForm, fields=('choice_text', 'is_correct_answer'), extra= question.n_choices)
#         #form = choices_formset()
#         form = ChoicesForm()
#         #form= choices_formset(queryset=Choice.objects.none(),)
#         return render(request, 'polls/create_answer.html', {'form': form})
#

def post_answer(request,question_id):
    question = Question.objects.get(pk=question_id)
    if question.question_type == 'T':
        choiceFormset = inlineformset_factory(Question, Choice, form=ChoicesForm_T, extra=question.n_choices)
    elif question.question_type == 'E':
        choiceFormset = inlineformset_factory(Question, Choice, form=ChoicesForm_E, extra=question.n_choices)
    elif question.question_type == 'D':
        return HttpResponseRedirect(reverse('polls:index'))

    if request.method == 'POST':
        form = choiceFormset(request.POST, instance = question)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('polls:index'))

    form = choiceFormset( instance = question)
    return render(request, 'polls/create_answer.html', {'form': form})

def results(request):
    users = User.objects.values_list('username',flat= True)
    user_list= []
    user_count = 0

    for user in users:
        profile=User.objects.get(username=user)
        if profile.is_staff == False:
            print(user)
            user_list.append(profile)
            user_count +=1


    return render(request, 'polls/results.html', {'user_list': user_list,'user_count': user_count})

def users_list(request):
    users = User.objects.values_list('username',flat= True)
    user_list= []
    user_count = 0
    datos_dic = is_student_dic =dict()
    for user in users:
        u = User.objects.get(username=user)
        if u.is_staff == False:
            datos_dic[user] = {"name": u.profile.nombre + " " + u.profile.apellido,"email": u.email,"subjects": u.profile.asignaturas.values_list('nombre',flat= True)}
            user_list.append(user)
            user_count += 1

    return render(request, 'polls/users_list.html',{'users_list': user_list,'user_count': user_count,'datos_dic':datos_dic})

def signup_teacher(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ModelForm_Teacher(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)

            profile.user = user
            profile.despacho = profile_form.cleaned_data['despacho']
            profile.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.first_name = form.cleaned_data.get('nombre')
            user.last_name = form.cleaned_data.get('apellido')
            user.email = form.cleaned_data.get('email')

            user.is_staff = True
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            print(user)
            g = Group.objects.get(name='Profesores')
            g.user_set.add(user)
            return redirect('polls:index')
    else:
        form = SignUpForm()
        profile_form = ModelForm_Teacher()

    return render(request, 'registration/signup_teacher.html', {'form': form, 'profile_form': profile_form})


def signup_student(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
      #  profile_form = ModelForm_Student(request.POST)
        #if form.is_valid() and profile_form.is_valid():
        if form.is_valid():
            user = form.save()
       #     profile = profile_form.save(commit=False)

        #    profile.user = user
        #    profile.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.first_name = form.cleaned_data.get('nombre')
            user.last_name = form.cleaned_data.get('apellido')
            user.email = form.cleaned_data.get('email')

            user.is_staff = False
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            print(user)
            g = Group.objects.get(name='Alumnos')
            g.user_set.add(user)
            return redirect('polls:index')
    else:
        form = SignUpForm()
        #profile_form = ModelForm_Student()

    #return render(request, 'registration/signup_teacher.html', {'form': form, 'profile_form': profile_form})
    return render(request, 'registration/signup_teacher.html', {'form': form})

@register.filter
def get_item(dictionary, key):
    print(dictionary.get(key))
    return dictionary.get(key)

def results_asignaturas(request):
    return render(request, 'polls/results_asignaturas.html')

def student_progress(request):
    students_progress= dict()
    # students_progress= dict()
    #     # students_progress={'Carlos Lechuga_1':{'votes_fail': 2,'votes_ok': 3}}
    #     # student_progress.append({'Carlos Lechuga_2':{'votes_fail': 3,'votes_ok': 4}})
    profiles = Profile.objects.all()
    print(profiles)
    for p in profiles:
        if p.user.is_staff == False:
            total_votes_FAIL= p.total_votes - p.total_votes_OK
            students_progress[p.nombre + " " + p.apellido ] = {'votes_FAIL': total_votes_FAIL,'votes_OK':p.total_votes_OK}

    print(f"Diccionario que pasamos: {students_progress}")
    return render(request, 'polls/student_progress.html',{'students_progress' : students_progress })

def export_csv_students(request):
    question_object = get_object_or_404(Profile, pk=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= "Resultado_global_tests_alumnos.csv"'
    writer = csv.writer(response, delimiter=';', dialect='excel')



    writer.writerow(['Nombre de Usuario', 'Nombre completo', 'Respuestas Correctas', 'Respuestas Incorrectas'])
    profiles=Profile.objects.all()
    for profile in profiles:
        if profile.user.is_staff == False:
            total_votes_FAIL = profile.total_votes - profile.total_votes_OK
            writer.writerow([profile.user.username, profile.nombre+" "+profile.apellido , profile.total_votes_OK, total_votes_FAIL])

    return response

def export_csv_test_result(request, question_id):
    question_object = get_object_or_404(Question, pk=question_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= ' + question_object.question_text + 'votos_alumnos.csv'
    writer = csv.writer(response, delimiter=';', dialect='excel')
    print(f"Todas las respuestas: {question_object.choice_set.all()}")
    for choice in question_object.choice_set.all():
        if choice.who_voted != None:
            print(choice.choice_text)
            writer.writerow([choice.choice_text])
            who_voted = ''.join(choice.who_voted)
            voters_list = who_voted.split(',')
            if '' in voters_list:
                voters_list.remove('')
            elif ' ' in voters_list:
                voters_list.remove(' ')
            print(f"Voters: {voters_list}")
            for voters in voters_list:
                print(voters)
                writer.writerow([voters])
            writer.writerow([' '])


    return response


def questions_list(request): # Es mejor poner las preguntas que ha creado el usuario

    department = request.user.profile.departamento
    print(request.user.profile.departamento) #Nos aseguramos de que el profesor solo pueda ver las asignaturas de su departamento
    subjects = Asignaturas.objects.filter(departamento = request.user.profile.departamento)
    questions_created= Question.objects.filter(creator = request.user.username)
    questions_dic= dict()

    for questions in questions_created:
        total_votes = 0
        for choice_list in questions.choice_set.all():
            total_votes += choice_list.votes
        questions_dic[questions]={'votes': total_votes,'pub_date': questions.pub_date.date()}


    print(f"Asignaturas de este departamento: {subjects }")
    return render(request, 'polls/questions_list.html',{'department':department, 'subjects':subjects,'questions_dic':questions_dic})

def delete_question(request,question_id):
    #borramos la pregunta en cuestión

    Question.objects.filter(id=question_id).delete()
    print("La pregunta ha sido borrada de la base de datos")
    #volvemos a la pagina

    department = request.user.profile.departamento
    print(request.user.profile.departamento) #Nos aseguramos de que el profesor solo pueda ver las asignaturas de su departamento
    subjects = Asignaturas.objects.filter(departamento = request.user.profile.departamento)
    questions_created= Question.objects.filter(creator = request.user.username)
    return redirect('/polls/questions_list/')


def save_answer_input(request,question_text):
    question = Question.objects.get(question_text= question_text)
    profile = get_object_or_404(Profile, pk=request.user.pk)
    if request.method == 'POST':

        form = Input_Answer(request.POST, instance = question)
        if form.is_valid():
            choice = Choice.objects.create(question= question)
            choice.save()
            choice.text_type_choice_text = form.cleaned_data.get('text_type_choice_text')
            choice.save()
            if choice.who_voted is None:
                who_voted = ''
                who_voted = profile.nombre + ' ' + profile.apellido
            choice.who_voted = who_voted
            choice.save()
            choice.votes = +1
            choice.save()
    return HttpResponseRedirect(reverse('polls:index'))

def detail_answer_input(request, question_text):
    answer_list = answer_list_context = []

    question = Question.objects.get(question_text=question_text)

    # for answer in question.choice_set.all():
    #     answer_list_context[answer.who_voted] = {'text':answer.text_type_choice_text}

    return render(request, 'polls/detail_text_questions.html', {'question': question})

def search(request):
    department = request.user.profile.departamento
    print(request.user.profile.departamento) #Nos aseguramos de que el profesor solo pueda ver las asignaturas de su departamento
    subjects = Asignaturas.objects.filter(departamento = request.user.profile.departamento)
    questions_list= Question.objects.filter(creator = request.user.username)

    question_filter = ChoiceFilter(request.GET, queryset=questions_list)

    #We must update the number of votes
    all_questions= Question.objects.all()

    for questions in all_questions:
        total_votes = 0
        for choice_list in questions.choice_set.all():
            total_votes += choice_list.votes
        questions.total_votes = total_votes
        questions.save()
    return render(request, 'polls/choice_list.html', {'filter': question_filter})



def GeneratePDF(request,question_id):
    question = Question.objects.get(pk= question_id)
    answers = question.choice_set.all()

    template = get_template('pdf_template.html')
    context = {
        "question" : question,
        "answers" : answers,
    }
    pdf = render_to_pdf('pdf_template.html',context)
    return HttpResponse(pdf, content_type='application/pdf')


def modify_question(request, question_id):
    question = get_object_or_404(Question, pk= question_id)
    #form = QuestionForm(instance=question)
    if request.method == 'POST':
        form = QuestionForm(request.POST,instance=question)

        if form.is_valid():
            post = form.save(commit=False)
            question_id = post.id
            post.creator = str(User.objects.get(username=request.user))
            post.save()



            return redirect('polls:post_answer', question_id = question_id)


    else:
        question = get_object_or_404(Question, pk=question_id)
        form = QuestionForm(instance= question)


    return render(request,'polls/create_question.html', {'form': form})


def modify_answer(request,question_id):
    question = Question.objects.get(pk=question_id)
    if question.question_type == 'T':
        choiceFormset = inlineformset_factory(Question, Choice, form=ChoicesForm_T, extra=question.n_choices)
    elif question.question_type == 'E':
        choiceFormset = inlineformset_factory(Question, Choice, form=ChoicesForm_E, extra=question.n_choices)
    elif question.question_type == 'D':
        return HttpResponseRedirect(reverse('polls:index'))

    if request.method == 'POST':
        form = choiceFormset(request.POST, instance = question)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('polls:index'))

    form = choiceFormset( instance = question)
    return render(request, 'polls/create_answer.html', {'form': form})