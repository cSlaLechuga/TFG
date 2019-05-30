"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from polls import views
from polls.views import ChartData



urlpatterns = [
    path('polls/', include('polls.urls'), name='polls'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup_teacher/', views.signup_teacher, name='signup_teacher'),
    path('signup_student/', views.signup_student, name='signup_student'),
    #path('api/chart/data/', ChartData.as_view(), name='api-chart-data')
    #path('api/chart/data/<uuid:pk>', ChartData.as_view(), name='api-chart-data')

]
