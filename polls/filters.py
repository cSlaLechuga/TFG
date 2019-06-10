import django_filters
from .models import Question

class ChoiceFilter(django_filters.FilterSet):
    class Meta:
        model = Question
        fields = ['asignatura','question_type', ]