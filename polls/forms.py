from django import forms
from .models import Question, Choice, Profile, User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from django.db import transaction
from django.forms import ModelForm,inlineformset_factory
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit,Div, Row, Column
from crispy_forms.bootstrap import Accordion, AccordionGroup, Field


# class QuestionForm(forms.ModelForm):
#
#
#
#     def __init__(self, *args, **kwargs):
#         super(QuestionForm, self).__init__(*args, **kwargs)
#         self.fields['question_text'].label = "Nueva Pregunta: "
#         self.fields['question_type'].label = "Tipo de pregunta: "
#         self.helper = FormHelper()
#         self.helper.form_show_labels = True
#         self.helper.form_tag = False
#         #self.helper.layout = Div('question_text')
#         #self.helper.layout = Div('question_text', title="Pregunta: ", css_class="col-sm-6 bg-success")
#         self.helper.layout = Layout(
#             Div(
#                 Div('question_text', title="Pregunta: ", label="Pregunta: ", css_class=" mb-2 mr-sm-2"),
#                 Div('question_type', css_class=' mb-2 mr-sm-2'),
#             css_class ='row align-items-center row h-100 justify-content-center mx-auto')
#         )
#
#     class Meta:
#         model = Question
#         fields = ('question_text', 'question_type')
#
#     class CustomModelChoiceField(forms.ModelChoiceField):
#         def label_from_instance(self, obj):
#             return "Pregunta: "

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

class QuestionForm(forms.ModelForm):
    question_text = forms.CharField(required=True, widget=forms.Textarea)
    n_choices = forms.IntegerField(required=True,widget=forms.NumberInput)
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['question_text'].label = "Nueva Pregunta "
        self.fields['question_type'].label = "Pregunta/Encuesta"
        self.fields['n_choices'].label = "Número de respuestas"
        # Making name required
        #self.fields['question_text'].required = True
        self.fields['asignatura'].required = True
        self.fields['question_type'].required = True

        self.fields['n_choices'].widget.attrs.update(size='10')

    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()
        question_text = cleaned_data.get('question_text')
        asignatura = cleaned_data.get('asignatura')
        question_type = cleaned_data.get('question_type')
        if not question_text and not asignatura and not question_type:
            raise forms.ValidationError('You have to write something!')

    class Meta:

        model= Question
        fields=('question_text','asignatura','question_type','n_choices')

class ChoicesForm_E(forms.ModelForm):

    def __init__(self, *args, **kwargs):


        super(ChoicesForm_E, self).__init__(*args, **kwargs)
        self.fields['choice_text'].label = ""





        # Making name required
        #self.fields['question_text'].required = True

        self.fields['choice_text'].required = True





    def clean(self):
        cleaned_data = super(ChoicesForm_E, self).clean()

        choice_text = cleaned_data.get('choice_text')
        is_correct_answer = cleaned_data.get('is_correct_answer')

        if not choice_text:
            raise forms.ValidationError('¡Cada pregunta debe tener una o mas respuestas!')

    class Meta:
        model = Choice
        fields = ('choice_text',)

class ChoicesForm_T(forms.ModelForm):

    def __init__(self, *args, **kwargs):


        super(ChoicesForm_T, self).__init__(*args, **kwargs)
        self.fields['choice_text'].label = ""
        self.fields['is_correct_answer'].label = "¿Es la respuesta correcta?"





        # Making name required
        #self.fields['question_text'].required = True

        self.fields['choice_text'].required = True





    def clean(self):
        cleaned_data = super(ChoicesForm_T, self).clean()

        choice_text = cleaned_data.get('choice_text')
        is_correct_answer = cleaned_data.get('is_correct_answer')

        if not choice_text:
            raise forms.ValidationError('¡Cada pregunta debe tener una o mas respuestas!')

    class Meta:
        model = Choice
        fields = ('choice_text','is_correct_answer')



class Input_Answer(forms.ModelForm):

    def __init__(self, *args, **kwargs):


        super(Input_Answer, self).__init__(*args, **kwargs)

        self.fields['text_type_choice_text'].label = ""
        self.fields['text_type_choice_text'].required = True





    def clean(self):
        cleaned_data = super(Input_Answer, self).clean()

        text_type_choice_text = cleaned_data.get('text_type_choice_text')


        if not text_type_choice_text:
            raise forms.ValidationError('¡Cada pregunta debe tener una o mas respuestas!')

    class Meta:
        model = Choice
        fields = ('text_type_choice_text',)

