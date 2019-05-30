from django import forms
from .models import Question, Choice, Profile, User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from django.db import transaction
from django.forms import ModelForm
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit,Div, Row, Column
from crispy_forms.bootstrap import Accordion, AccordionGroup, Field


class QuestionForm(forms.ModelForm):



    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['question_text'].label = "Nueva Pregunta: "
        self.fields['question_type'].label = "Tipo de pregunta: "
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.form_tag = False
        #self.helper.layout = Div('question_text')
        #self.helper.layout = Div('question_text', title="Pregunta: ", css_class="col-sm-6 bg-success")
        self.helper.layout = Layout(
            Div(
                Div('question_text', title="Pregunta: ", label="Pregunta: ", css_class=" mb-2 mr-sm-2"),
                Div('question_type', css_class=' mb-2 mr-sm-2'),
            css_class ='row align-items-center row h-100 justify-content-center mx-auto')
        )

    class Meta:
        model = Question
        fields = ('question_text', 'question_type')

    class CustomModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return "Pregunta: "

class ChoicesForm(forms.ModelForm):



    def __init__(self, *args, **kwargs):
        super(ChoicesForm, self).__init__(*args, **kwargs)
        self.fields['choice_text'].label = "Nueva Respuesta: "
        self.fields['is_correct_answer'].label = "¿Es respuesta correcta?"
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.form_tag = False
        self.helper.form_action = "post_question"
        self.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Column('choice_text', css_class=" mb-2 mr-sm-2"),
                Column('is_correct_answer', css_class='custom-control custom-radio'),
            css_class ='row')
        )


    class Meta:
        model = Choice
        fields = ('choice_text', 'is_correct_answer')


class SignUpForm(UserCreationForm):
   nombre = forms.CharField(max_length=100)
   apellido = forms.CharField(max_length=100)
   email= forms.EmailField(max_length=20)


   class Meta:
       model= User
       fields = ('username', 'email','nombre','apellido' , 'password1', 'password2',)


class ModelForm_Teacher(forms.ModelForm):
   despacho = forms.CharField(max_length=10)


   class Meta:
       model= Profile
       fields = ('despacho',)

# class ModelForm_Student(forms.ModelForm):
#
#     class Meta:
#         model = Profile
