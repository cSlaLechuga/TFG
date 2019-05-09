from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<uuid:question_id>/', views.detail, name='detail'),
    path('<uuid:question_id>/results/', views.results, name='results'),
    path('<uuid:question_id>/vote/', views.vote, name='vote'),

]