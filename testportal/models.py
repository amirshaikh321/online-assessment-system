from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=250)
    option1 = models.CharField(max_length=250)
    option2 = models.CharField(max_length=250)
    option3 = models.CharField(max_length=250)
    option4 = models.CharField(max_length=250)
    correct_option = models.CharField(max_length=250)

    class Meta:
        db_table = 'question'

class student(models.Model):
    name = models.CharField(max_length=100)
    rollno = models.IntegerField()
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=250)

    class Meta:
        db_table = 'student'

class Admin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=250)

    class Meta:
        db_table = 'admin'