

from django.contrib import admin

from .models import Question, Choice
from django.shortcuts import get_object_or_404


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3
    list_display = ('choice_text', 'votes', 'id')
    if Question.question_type =='Tipo Test':
        list_display = ('choice_text', 'votes', 'id','is_correct_answer')


class QuestionAdmin(admin.ModelAdmin):
    list_display= ('question_text', 'id', 'pub_date','question_type')

    #fields = ['pub_date','question_text']
    readonly_fields = ['pub_date']
    inlines=[ChoiceInLine]
admin.site.register(Question, QuestionAdmin)

