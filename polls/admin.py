from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib import admin

from .models import Question, Choice, Profile, Asignaturas, Departamento
from django.shortcuts import get_object_or_404


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3
    list_display = ('choice_text', 'votes', 'id')
    if Question.question_type =='Tipo Test':
        list_display = ('choice_text', 'votes', 'id','is_correct_answer','text_type_choice_text')


class QuestionAdmin(admin.ModelAdmin):
    list_display= ('question_text', 'id', 'pub_date','question_type')

    #fields = ['pub_date','question_text']
    readonly_fields = ['pub_date']
    inlines=[ChoiceInLine]
admin.site.register(Question, QuestionAdmin)




admin.site.register(Profile)
admin.site.register(Asignaturas)
admin.site.register(Departamento)



