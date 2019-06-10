

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid





class Departamento(models.Model):
    nombre = models.CharField(default='', null=True, max_length=100, help_text="Nombre del departamento")
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Identificador unico del departamento")


    def __str__(self):
        return self.nombre


class Asignaturas(models.Model):
    nombre= models.TextField(max_length=200, help_text="Asignatura")
    codigo= models.CharField(max_length=10, help_text="Codigo de la asignatura")
    departamento= models.ForeignKey(Departamento, on_delete=models.CASCADE)
    #alumnos= models.ManyToManyField()

    def __str__(self):
        return self.nombre


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Identificador unico de la pregunta")
    pub_date = models.DateTimeField(auto_now_add=True)
    asignatura= models.ForeignKey(Asignaturas,on_delete=models.CASCADE)
    creator = models.CharField(max_length=200, null=True, blank=True)
    n_choices = models.IntegerField(null=True, blank=True)
    total_votes = models.IntegerField(null=True, blank=True)

    ENCUESTA = 'E'
    TEST = 'T'
    DESARROLLO = 'D'
    QUESTION_TYPE = (
        (ENCUESTA, 'Encuesta'),
        (TEST, 'Tipo Test'),
        (DESARROLLO, 'Desarrollo'),
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
    choice_text = models.CharField(max_length=200,null=True, blank=True)
    text_type_choice_text = models.TextField(max_length=1000,null=True, blank=True)
    votes = models.IntegerField(default=0)
    choice_id = models.UUIDField(primary_key=True, default=uuid.uuid1, help_text="Identificador unico de la respuesta")
    is_correct_answer = models.BooleanField(default=False)
    who_voted = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.text_type_choice_text:

            return self.text_type_choice_text
        return str(self.choice_text)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    is_docente= models.BooleanField(default=False)
    is_alumno= models.BooleanField(default=False)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    asignaturas= models.ManyToManyField(Asignaturas)
    despacho = models.CharField(max_length=200, null=True, blank=True)
    departamento= models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
    total_votes = models.IntegerField(default=0)
    total_votes_OK = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


