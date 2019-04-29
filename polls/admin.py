

from django.contrib import admin

from .models import Question, Choice


class ChoiceInLine(admin.TabularInline):
    model=Choice
    extra=3
    list_display = ('choice_text', 'votes')

class QuestionAdmin(admin.ModelAdmin):
    list_display= ('question_text', 'id', 'pub_date')
    #fields = ['pub_date','question_text']
    readonly_fields = ['pub_date']
    inlines=[ChoiceInLine]
admin.site.register(Question, QuestionAdmin)
#class ChoiceAdmin(admin.ModelAdmin):


