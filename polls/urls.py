from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<uuid:question_id>/', views.detail, name='detail'),
    path('results/', views.results, name='results'),
    path('<uuid:question_id>/vote/', views.vote, name='vote'),
    path('<uuid:question_id>/export_csv/', views.export_csv, name='export_csv'),
    path('create_question/', views.post_question, name='post_question'),
    path('create_question/<uuid:question_id>/create_answer/', views.post_answer, name='post_answer'),
    path('results/users_list/', views.users_list, name= 'users_list')
    #path('<uuid:question_id>/api/chart/data/', views.ChartData.as_view(), name='api-chart-data')

]