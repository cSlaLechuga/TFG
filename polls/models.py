

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

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete="models.CASCADE", related_name='teacher_profile')
    name = models.CharField(max_length=200, help_text="Nombre del profesor")
    last_name = models.CharField(max_length=200, help_text="Apellido del profesor")

    def __str__(self):
        return self.name + self.last_name



