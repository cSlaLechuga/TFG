

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid




class Question(models.Model):
    question_text = models.CharField(max_length=200)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Identificador unico de la pregunta")
    pub_date = models.DateTimeField(auto_now_add=True)
    ENCUESTA = 'E'
    TEST = 'T'
    QUESTION_TYPE = (
        (ENCUESTA, 'Encuesta'),
        (TEST, 'Tipo Test'),
    )
    question_type = models.CharField(
        max_length=1,
        choices=QUESTION_TYPE,
        default=ENCUESTA
    )



    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    choice_id = models.UUIDField(primary_key=True, default=uuid.uuid1, help_text="Identificador unico de la respuesta")
    is_correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text
class Departamento(models.Model):
    nombre=models.CharField(max_length=30, help_text="Nombre del departamento")


    def __str__(self):
        return self.nombre


class Asignaturas(models.Model):
    nombre= models.CharField(max_length=200, help_text="Asignatura")
    codigo= models.CharField(max_length=10, help_text="Codigo de la asignatura")
    departamento= models.ForeignKey(Departamento, on_delete=models.CASCADE)
    #alumnos= models.ManyToManyField()

    def __str__(self):
        return self.nombre



# class Profesores(models.Model):
#     user = models.OneToOneField(User, on_delete="models.CASCADE")
#     nombre = models.CharField(max_length=200, help_text="Nombre del profesor")
#     is_docente= models.BooleanField(default=True)
#     apellido = models.CharField(max_length=200, help_text="Apellido del profesor")
#     asignaturas= models.ManyToManyField(Asignaturas)
#     departamento= models.ForeignKey(Departamento,on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.nombre + self.apellido

class Alumno(models.Model):
    #user = models.OneToOneField(User, on_delete="models.CASCADE", primary_key=True)
    is_docente= models.BooleanField(default=False)
    nombre = models.CharField(max_length=200, help_text="Nombre del alumno")
    apellido = models.CharField(max_length=200, help_text="Apellido del alumno")
    asignaturas= models.ManyToManyField(Asignaturas)
    departamento= models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + self.apellido





