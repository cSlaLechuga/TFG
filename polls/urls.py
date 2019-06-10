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
    path('create_question/<uuid:question_id>/post_answer/', views.post_answer, name='post_answer'),
    path('results/users_list/', views.users_list, name= 'users_list'),
    path('results_asignaturas/', views.results_asignaturas, name='results_asignaturas'),
    path('student_progress/', views.student_progress, name='student_progress'),
    path('student_progress/export_csv_students/',views.export_csv_students, name='export_csv_students'),
    path('<uuid:question_id>/export_csv_test_result/',views.export_csv_test_result, name='export_csv_test_result'),
    #path('questions_list/', views.questions_list, name='questions_list'),
    path('<uuid:question_id>/delete/', views.delete_question, name='delete_question'),
    path('<str:question_text>/save_answer_input/', views.save_answer_input, name='save_answer_input'),
    path('<str:question_text>/detail_text_type/', views.detail_answer_input, name='detail_answer_input'),
    path('questions_list/', views.search, name='search'),
    path('<uuid:question_id>/pdf/', views.GeneratePDF, name='GeneratePDF'),
    path('<uuid:question_id>/modify_question/', views.modify_question, name='modify_question'),
    path('<uuid:question_id>/modify_answer/', views.modify_answer, name='modify_answer'),
    path('results/users_list_staff/', views.users_list_staff, name= 'users_list_staff'),
    path('results/<str:username>/send_email/', views.send_email, name= 'send_email'),


    #path('<uuid:question_id>/api/chart/data/', views.ChartData.as_view(), name='api-chart-data')

]